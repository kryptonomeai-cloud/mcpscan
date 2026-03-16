# Email Classifier Dashboard + Trivy Fix — 2026-03-14

## Task 1: Email Classifier Dashboard ✅

### Setup
- **Project:** `/Users/miniclaw/.openclaw/workspace/projects/email-classifier-dashboard/`
- **Framework:** Next.js 16.1.6 + TypeScript + Tailwind CSS (App Router)
- **Theme:** Dark (#0a0a0b background, #06b6d4 cyan accents) — matches MindFizz

### Features
- **Stats cards:** Total classified (15,052), categories (30), avg confidence, top category
- **Bar chart:** All 30 categories with counts, percentages, gradient bars
- **Email table:** Date, subject, from, category badge, confidence bar
- **Search:** Free-text search across subject/sender
- **Filter:** Dropdown filter by any of 30 categories with counts
- **Responsive:** Works on desktop and mobile

### Data
- Mock dataset generated based on realistic distribution across 30 categories
- Categories: AI/ML, Finance, Shopping, Travel, Health, Legal, Education, Social, News, Promotions, Updates, Security, Work, Personal, Receipts, Subscriptions, Government, Insurance, Banking, Utilities, Real Estate, Automotive, Food, Entertainment, Sports, Technology, Communication, Career, Family, Other
- 200 sample emails with realistic subjects, senders, dates, and confidence scores
- Ready to swap with real JSONL data from `emails-master.jsonl`

### Run
```bash
cd projects/email-classifier-dashboard
npm run dev    # → http://localhost:3000
npm run build  # ✅ builds successfully
```

---

## Task 2: Trivy DB Fix ✅

### Problem
- Trivy vulnerability DB was 13 days stale (since Mar 1, 2026)
- DB download failed with credential errors — Docker Desktop's `credsStore: "desktop"` credential helper was timing out

### Root Cause
Docker config (`~/.docker/config.json`) uses `"credsStore": "desktop"` but Docker Desktop wasn't fully responsive, causing the credential helper to hang and get killed by the 30s timeout.

### Fix
Bypassed Docker credential store by pointing to empty config:
```bash
mkdir -p /tmp/trivy-docker && echo '{}' > /tmp/trivy-docker/config.json
DOCKER_CONFIG=/tmp/trivy-docker trivy image --download-db-only --db-repository ghcr.io/aquasecurity/trivy-db:2
```

### Result
- DB downloaded successfully (87.78 MiB, ~4 seconds at 35+ MiB/s)
- Repository: `ghcr.io/aquasecurity/trivy-db:2`
- Test scan on `alpine:latest` found 1 CRITICAL vulnerability:
  - **CVE-2026-22184**: zlib arbitrary code execution via buffer overflow (fixed in 1.3.2-r0)

### Recommended Permanent Fix
Add to shell profile or alias:
```bash
alias trivy='DOCKER_CONFIG=/tmp/trivy-docker trivy'
```
Or fix Docker Desktop credential store by ensuring Docker Desktop is running when Trivy updates.
