"""HMRC Tax Advisor — FastAPI backend wrapping RAG pipeline."""
from __future__ import annotations

import re
import time
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Config ──────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434"
QDRANT_URL = "http://192.168.0.18:6333"
COLLECTION = "hmrc-manuals"
EMBED_MODEL = "bge-m3"
LLM_MODEL = "qwen3:32b"

INITIAL_FETCH = 20
RERANK_TOP = 7
FINAL_TOP = 5
MAX_XREFS = 3
CONTEXT_MAX_CHARS = 8000
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ── App ─────────────────────────────────────────────────────────────
app = FastAPI(title="HMRC Tax Advisor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup warmup ──────────────────────────────────────────────────
@app.on_event("startup")
async def warmup():
    """Pre-warm the embedding model so Ollama doesn't need to swap on first request."""
    try:
        requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": "warmup"},
            timeout=300,
        )
        print(f"✓ {EMBED_MODEL} warmed up")
    except Exception as e:
        print(f"Warning: could not warm up embedding model: {e}")


# ── Lazy globals ────────────────────────────────────────────────────
_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        try:
            from sentence_transformers import CrossEncoder
            _reranker = CrossEncoder(RERANKER_MODEL)
        except Exception:
            _reranker = False
    return _reranker if _reranker is not False else None


# ── Models ──────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str


class Citation(BaseModel):
    section_id: str
    manual: str
    title: str
    url: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: str  # HIGH | MEDIUM | LOW
    confidence_score: float
    elapsed: float


# ── Embedding ───────────────────────────────────────────────────────
def get_embedding(text: str) -> list[float]:
    resp = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def unload_embed_model() -> None:
    """Unload bge-m3 from VRAM before calling the LLM.

    On Apple Silicon, having both bge-m3 and qwen3:32b loaded simultaneously
    triggers a Metal GGML assertion crash (rsets->data count == 0).
    Sending keep_alive=0 forces Ollama to evict it before the LLM loads.
    """
    try:
        requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": "", "keep_alive": 0},
            timeout=30,
        )
        print(f"✓ {EMBED_MODEL} unloaded from VRAM")
    except Exception as e:
        print(f"Warning: could not unload {EMBED_MODEL}: {e}")


# ── Search ──────────────────────────────────────────────────────────
def search_semantic(vector: list[float], limit: int = INITIAL_FETCH,
                    manual_filter: Optional[str] = None) -> list[dict]:
    payload = {"vector": vector, "limit": limit, "with_payload": True}
    if manual_filter:
        payload["filter"] = {
            "must": [{"key": "manual_name", "match": {"value": manual_filter}}]
        }
    resp = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        json=payload, timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("result", [])


def search_keyword(query: str, limit: int = INITIAL_FETCH) -> list[dict]:
    words = [w for w in query.split() if len(w) > 2][:8]
    if not words:
        return []
    conditions = [{"key": "content", "match": {"text": w}} for w in words]
    payload = {
        "filter": {"should": conditions},
        "limit": limit,
        "with_payload": True,
        "with_vector": False,
    }
    resp = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll",
        json=payload, timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("result", {}).get("points", [])


def normalize_results(results: list[dict], source: str) -> list[dict]:
    out = []
    for r in results:
        p = r.get("payload", {})
        out.append({
            "section_id": p.get("section_id", ""),
            "manual": p.get("manual_name", ""),
            "title": p.get("title", ""),
            "score": r.get("score", 0.5),
            "content": p.get("content", ""),
            "source": source,
        })
    return out


def deduplicate(results: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for r in results:
        sid = r["section_id"]
        if sid and sid not in seen:
            seen.add(sid)
            out.append(r)
    return out


# ── Re-ranking ──────────────────────────────────────────────────────
def rerank(query: str, results: list[dict], top_n: int = RERANK_TOP) -> list[dict]:
    ranker = get_reranker()
    if not ranker or not results:
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

    pairs = []
    for r in results:
        doc_text = f"{r['title']}. {r['content'][:500]}"
        pairs.append((query, doc_text))

    scores = ranker.predict(pairs)
    for i, r in enumerate(results):
        r["rerank_score"] = float(scores[i])
        r["original_score"] = r["score"]

    results.sort(key=lambda x: x["rerank_score"], reverse=True)
    return results[:top_n]


# ── Query Expansion ─────────────────────────────────────────────────
def expand_query(query: str) -> list[str]:
    prompt = (
        "Given this tax question, generate 2 alternative search queries using HMRC/UK tax terminology.\n"
        "Return ONLY the queries, one per line. No numbering, no explanation.\n\n"
        f"Question: {query}\n\nAlternative queries:"
    )
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": LLM_MODEL, "keep_alive": "24h",
                "prompt": prompt,
                "stream": False, "think": False,
                "options": {"temperature": 0.3, "num_predict": 150},
            },
            timeout=300,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "") or data.get("thinking", "")
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        lines = [l.strip().lstrip("0123456789.-) ") for l in text.strip().split("\n") if l.strip()]
        return [l for l in lines if len(l) > 5][:2]
    except Exception:
        return []


# ── Cross-References ────────────────────────────────────────────────
def extract_xrefs(content: str) -> list[str]:
    pattern = r'\b([A-Z]{2,5}\d{4,6})\b'
    return list(set(re.findall(pattern, content)))


def fetch_section_by_id(section_id: str) -> Optional[dict]:
    payload = {
        "filter": {
            "must": [{"key": "section_id", "match": {"value": section_id.lower()}}]
        },
        "limit": 1,
        "with_payload": True,
        "with_vector": False,
    }
    try:
        resp = requests.post(
            f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll",
            json=payload, timeout=60,
        )
        resp.raise_for_status()
        points = resp.json().get("result", {}).get("points", [])
        if points:
            p = points[0]["payload"]
            return {
                "section_id": p.get("section_id", ""),
                "manual": p.get("manual_name", ""),
                "title": p.get("title", ""),
                "score": 0.8,
                "content": p.get("content", ""),
                "source": "xref",
            }
    except Exception:
        pass
    return None


def follow_cross_references(results: list[dict], existing_ids: set) -> list[dict]:
    xref_results = []
    xref_count = 0
    for r in results:
        if xref_count >= MAX_XREFS:
            break
        refs = extract_xrefs(r["content"])
        for ref_id in refs:
            if ref_id.lower() in existing_ids or xref_count >= MAX_XREFS:
                continue
            fetched = fetch_section_by_id(ref_id)
            if fetched:
                existing_ids.add(fetched["section_id"])
                xref_results.append(fetched)
                xref_count += 1
    return xref_results


# ── Manual Detection ────────────────────────────────────────────────
MANUAL_KEYWORDS = {
    "capital-gains-manual": ["CGT", "capital gains", "disposal", "chargeable gain"],
    "business-income-manual": ["trading", "business expense", "trade profit", "BIM"],
    "employment-income-manual": ["employment", "PAYE", "salary", "employee", "employer"],
    "vat-manual": ["VAT", "value added tax", "registration threshold", "input tax"],
    "income-tax-manual": ["income tax", "personal allowance", "tax band", "tax rate"],
    "self-assessment-manual": ["self assessment", "tax return", "SA"],
    "stamp-duty-manual": ["stamp duty", "SDLT", "land tax"],
    "inheritance-tax-manual": ["inheritance tax", "IHT", "estate"],
}


def detect_manual(query: str) -> Optional[str]:
    query_lower = query.lower()
    scores = {}
    for manual, keywords in MANUAL_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in query_lower)
        if score > 0:
            scores[manual] = score
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] >= 2:
            return best
    return None


# ── Confidence ──────────────────────────────────────────────────────
def compute_confidence(results: list[dict]) -> dict:
    if not results:
        return {"level": "LOW", "score": 0.0}

    avg_orig = sum(r.get("original_score", r["score"]) for r in results) / len(results)
    top_orig = max(r.get("original_score", r["score"]) for r in results)
    top_rerank = max(r.get("rerank_score", 0) for r in results)
    n_results = len(results)
    unique_manuals = len(set(r["manual"] for r in results))

    conf_score = 0.0
    if top_orig > 0.7:
        conf_score += 0.3
    elif top_orig > 0.6:
        conf_score += 0.2
    elif top_orig > 0.5:
        conf_score += 0.1

    if avg_orig > 0.6:
        conf_score += 0.2
    elif avg_orig > 0.5:
        conf_score += 0.1

    if top_rerank > 0:
        conf_score += 0.2
    elif top_rerank > -3:
        conf_score += 0.1

    if n_results >= 3:
        conf_score += 0.15

    if unique_manuals >= 2:
        conf_score += 0.1

    if any(r["source"] == "xref" for r in results):
        conf_score += 0.1

    conf_score = min(conf_score, 1.0)

    if conf_score >= 0.65:
        level = "HIGH"
    elif conf_score >= 0.35:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {"level": level, "score": round(conf_score, 2)}


# ── LLM Answer ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an HMRC tax information assistant. Your role is to provide accurate information based ONLY on the official HMRC manual sections provided below.

Rules:
1. Answer based ONLY on the provided HMRC manual sections. Do not use external knowledge.
2. ALWAYS cite specific section IDs (e.g., EIM32760, BIM47825) when making claims.
3. If the provided sections don't contain enough information to answer fully, say so explicitly.
4. Never give personal tax advice. Always frame answers as "HMRC guidance states..." or "According to section X..."
5. If the question requires professional judgement, recommend consulting a tax adviser.
6. Be precise about tax years, thresholds, and rates — only state figures that appear in the sources.
7. Format your answer clearly with section references in parentheses."""


def build_context(results: list[dict]) -> str:
    context_parts = []
    total_chars = 0
    for r in results:
        section_text = (
            f"--- Section: {r['section_id'].upper()} ---\n"
            f"Manual: {r['manual']}\nTitle: {r['title']}\n"
            f"Content:\n{r['content']}\n"
        )
        if total_chars + len(section_text) > CONTEXT_MAX_CHARS:
            remaining = CONTEXT_MAX_CHARS - total_chars - 100
            if remaining > 200:
                section_text = section_text[:remaining] + "\n[truncated]\n"
            else:
                break
        context_parts.append(section_text)
        total_chars += len(section_text)
    return "\n".join(context_parts)


def generate_answer(query: str, results: list[dict], confidence: dict) -> str:
    context = build_context(results)
    confidence_note = ""
    if confidence["level"] == "LOW":
        confidence_note = "\nNote: The retrieval confidence is LOW. Be extra cautious and clearly state limitations."
    elif confidence["level"] == "MEDIUM":
        confidence_note = "\nNote: The retrieval confidence is MEDIUM. Some aspects may not be fully covered by the sources."

    user_prompt = (
        f"Based on the following HMRC manual sections, answer this question:\n\n"
        f"Question: {query}\n{confidence_note}\n\n"
        f"=== HMRC Manual Sections ===\n{context}\n=== End of Sections ===\n\n"
        f"Provide a clear, well-cited answer. If information is incomplete, say so."
    )

    try:
        payload = {
            "model": LLM_MODEL, "keep_alive": "24h",
            "system": SYSTEM_PROMPT,
            "prompt": user_prompt,
            "stream": False, "think": False,
            "options": {"temperature": 0.1, "num_predict": 1500},
        }
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=300,
        )
        if resp.status_code != 200:
            print(f"Ollama generate error {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("response", "") or data.get("thinking", "")
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
        return answer
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating answer: {e}"


def make_citation_url(manual: str, section_id: str) -> str:
    """Build gov.uk link for HMRC manual section."""
    return f"https://www.gov.uk/hmrc-internal-manuals/{manual}/{section_id}"


# ── Pipeline ────────────────────────────────────────────────────────
def run_pipeline(question: str) -> AskResponse:
    t0 = time.time()

    # Manual detection
    manual_filter = detect_manual(question)

    # Search with original query only (skip query expansion to avoid
    # extra LLM↔embedding model swap which causes timeouts on single-GPU)
    all_results = []
    vec = get_embedding(question)
    sem = search_semantic(vec, INITIAL_FETCH, manual_filter)
    all_results.extend(normalize_results(sem, "semantic"))
    kw = search_keyword(question, INITIAL_FETCH // 2)
    all_results.extend(normalize_results(kw, "keyword"))

    if manual_filter:
        sem_all = search_semantic(vec, INITIAL_FETCH // 2)
        all_results.extend(normalize_results(sem_all, "semantic-broad"))

    all_results = deduplicate(all_results)

    # Re-rank
    ranked = rerank(question, all_results, RERANK_TOP)

    # Cross-references
    existing_ids = {r["section_id"] for r in ranked}
    xrefs = follow_cross_references(ranked[:3], existing_ids)
    ranked.extend(xrefs)

    final_results = ranked[:FINAL_TOP]

    # Confidence
    confidence = compute_confidence(final_results)

    # Unload bge-m3 before calling qwen3:32b — both in VRAM simultaneously
    # causes a Metal GPU assertion crash on Apple Silicon.
    unload_embed_model()

    # Generate answer
    answer = generate_answer(question, final_results, confidence)

    # Build citations
    citations = []
    for r in final_results:
        citations.append(Citation(
            section_id=r["section_id"].upper(),
            manual=r["manual"],
            title=r["title"],
            url=make_citation_url(r["manual"], r["section_id"]),
        ))

    elapsed = round(time.time() - t0, 1)

    return AskResponse(
        answer=answer,
        citations=citations,
        confidence=confidence["level"],
        confidence_score=confidence["score"],
        elapsed=elapsed,
    )


# ── Endpoints ───────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    """Health check — verifies Qdrant and Ollama are reachable."""
    status = {"status": "ok", "qdrant": False, "ollama": False}
    try:
        r = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}", timeout=5)
        status["qdrant"] = r.status_code == 200
    except Exception:
        pass
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        status["ollama"] = r.status_code == 200
    except Exception:
        pass
    if not status["qdrant"] or not status["ollama"]:
        status["status"] = "degraded"
    return status


@app.post("/api/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        return run_pipeline(req.question.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
