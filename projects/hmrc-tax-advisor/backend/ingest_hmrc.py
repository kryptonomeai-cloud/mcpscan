#!/usr/bin/env python3
"""
HMRC Tax Advisor — Qdrant Ingestion Script
Scrapes key HMRC internal manuals from gov.uk and loads into Qdrant.
"""
import json, os, time, re, uuid, sys, requests
from typing import Optional

QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
COLLECTION = "hmrc-manuals"
EMBED_MODEL = "bge-m3"
EMBED_DIM = 1024
BATCH_SIZE = 20

# Key HMRC manuals to ingest (manual_slug: display_name)
MANUALS = {
    "employment-income-manual": "Employment Income Manual",
    "capital-gains-manual": "Capital Gains Manual", 
    "inheritance-tax-manual": "Inheritance Tax Manual",
    "vat-guide-notice-700": None,  # skip - different structure
    "paye-manual": "PAYE Manual",
    "business-income-manual": "Business Income Manual",
    "national-insurance-manual": "National Insurance Manual",
    "self-assessment-manual": "Self Assessment Manual",
}

SEED_URLS = {
    "employment-income-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim00500",
        "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim01000",
        "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11100",
        "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim20000",
        "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim40000",
    ],
    "capital-gains-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg10000",
        "https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg14200",
        "https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg50000",
        "https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg60000",
    ],
    "inheritance-tax-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm10000",
        "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm04000",
    ],
    "paye-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye10000",
        "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye20000",
    ],
    "business-income-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/business-income-manual/bim00000",
        "https://www.gov.uk/hmrc-internal-manuals/business-income-manual/bim45000",
    ],
    "national-insurance-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim01001",
    ],
    "self-assessment-manual": [
        "https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual/sam10000",
    ],
}

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; HMRC-RAG-Bot/1.0)"})


def get_embedding(text: str) -> list:
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text[:4000]},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["embedding"]


def scrape_section(url: str, manual_slug: str) -> Optional[dict]:
    """Scrape a single HMRC manual section page."""
    try:
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            return None
        
        # Extract section id from URL
        section_id = url.rstrip("/").split("/")[-1].upper()
        
        # Basic text extraction using regex (no beautifulsoup needed)
        html = r.text
        
        # Extract title
        title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else section_id
        
        # Extract main content (article or main body)
        content_m = re.search(r'<div[^>]*class="[^"]*govuk-body[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if not content_m:
            # Try article tag
            content_m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if not content_m:
            # Try main
            content_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        
        if content_m:
            content_raw = content_m.group(1)
            # Strip HTML tags
            content = re.sub(r'<[^>]+>', ' ', content_raw)
            content = re.sub(r'\s+', ' ', content).strip()
            # Remove navigation noise
            content = re.sub(r'(Previous|Next|Contents)\s*$', '', content).strip()
        else:
            content = title
        
        if len(content) < 50:
            return None
            
        manual_name = MANUALS.get(manual_slug, manual_slug)
        
        return {
            "section_id": section_id,
            "manual_name": manual_name or manual_slug,
            "title": title[:200],
            "content": content[:3000],
            "url": url,
        }
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return None


def create_collection():
    """Create Qdrant collection if not exists."""
    # Check if exists
    r = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}", timeout=10)
    if r.status_code == 200:
        print(f"Collection '{COLLECTION}' already exists")
        info = r.json()
        count = info.get("result", {}).get("points_count", 0)
        print(f"  Current points: {count}")
        return
    
    # Create
    payload = {
        "vectors": {
            "size": EMBED_DIM,
            "distance": "Cosine",
        },
        "payload_schema": {
            "manual_name": {"data_type": "keyword"},
            "section_id": {"data_type": "keyword"},
            "content": {"data_type": "text"},
        }
    }
    r = requests.put(f"{QDRANT_URL}/collections/{COLLECTION}", json=payload, timeout=30)
    r.raise_for_status()
    print(f"Created collection '{COLLECTION}'")
    
    # Create payload index for full-text search
    for field in ["content", "manual_name"]:
        idx_payload = {"field_name": field, "field_schema": "text" if field == "content" else "keyword"}
        requests.put(f"{QDRANT_URL}/collections/{COLLECTION}/index", json=idx_payload, timeout=10)
    print("Created indexes")


def upsert_batch(points: list):
    """Upload a batch of points to Qdrant."""
    r = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        json={"points": points},
        timeout=120,
    )
    r.raise_for_status()


def main():
    print("=== HMRC Tax Advisor — Qdrant Ingestion ===\n")
    
    # Create collection
    create_collection()
    
    total = 0
    for manual_slug, seed_urls in SEED_URLS.items():
        if MANUALS.get(manual_slug) is None:
            continue
        print(f"\n📖 Manual: {MANUALS[manual_slug]}")
        
        batch = []
        for url in seed_urls:
            print(f"  Scraping {url}...")
            section = scrape_section(url, manual_slug)
            if not section:
                print(f"  → skipped (empty/failed)")
                continue
            
            # Get embedding
            try:
                vec = get_embedding(section["content"])
            except Exception as e:
                print(f"  → embedding failed: {e}")
                continue
            
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
            batch.append({
                "id": point_id,
                "vector": vec,
                "payload": {
                    "section_id": section["section_id"],
                    "manual_name": section["manual_name"],
                    "title": section["title"],
                    "content": section["content"],
                },
            })
            print(f"  → '{section['title'][:60]}' ({len(section['content'])} chars)")
            total += 1
            
            if len(batch) >= BATCH_SIZE:
                upsert_batch(batch)
                print(f"  ↑ Uploaded {len(batch)} points")
                batch = []
            
            time.sleep(0.5)  # polite scraping
        
        if batch:
            upsert_batch(batch)
            print(f"  ↑ Uploaded {len(batch)} points")
    
    print(f"\n✅ Done! Ingested {total} sections total.")
    
    # Final check
    r = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}", timeout=10)
    if r.status_code == 200:
        count = r.json().get("result", {}).get("points_count", 0)
        print(f"Collection now has {count} points.")


if __name__ == "__main__":
    main()
