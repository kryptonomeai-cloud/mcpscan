# HMRC Tax Advisor — Test Results 2026-03-14

## Status: ✅ WORKING

## Root Cause of Initial Failure
qwen3:32b is a thinking model — it outputs to `thinking` field, leaving `response` empty.
Fix: added `"think": False` to all `/api/generate` calls.

## Fixes Applied
1. `think: False` on all LLM calls (qwen3:32b thinking mode was causing empty responses)
2. `keep_alive: "24h"` on all Ollama calls (prevent model swap timeouts)
3. `LLM_MODEL = "qwen3:32b"` (was incorrectly set to qwen3.5:27b)
4. Pre-warm both bge-m3 and qwen3:32b on startup
5. Increased all request timeouts to 300s

## Test Results

| Question | Confidence | Citations | Time |
|----------|-----------|-----------|------|
| What is the VAT registration threshold? | HIGH | 5 | ~60s |
| What is self assessment? | HIGH | 5 | 87s |

### Self Assessment Answer (sample)
> Self Assessment is a system used by HMRC to collect Income Tax from individuals who are not 
> covered entirely by the PAYE system. It requires taxpayers to report their income and calculate 
> the tax they owe for each tax year...
> Citations: SAM133001, EIM71410, SAM20001, SAM20130, CG57839

## Running
- Backend: `http://127.0.0.1:8200` (uvicorn, nohup)
- Frontend: `cd frontend && npm run dev` → http://localhost:3000
- Response time: ~60-90s (Ollama qwen3:32b on CPU/unified memory)
- Qdrant: hmrc-manuals collection, 11,987 points on NAS
