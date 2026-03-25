
---
## 2026-03-17 07:45 UTC — Daily Monitor

### Version
- **Installed:** 2026.3.13 (61d171a)
- **Latest on GitHub:** 2026.3.13-1 (recovery release, published 2026-03-14)
  - The `-1` suffix is a GitHub/tag-only fix; npm version is still `2026.3.13` — **no update needed**
  - Notable fixes in this release:
    - `fix(telegram)`: thread media transport policy into SSRF — minor security hardening
    - `fix(compaction)`: full-session token count for post-compaction sanity check
    - `fix(session)`: preserve lastAccountId and lastThreadId on session reset
    - `fix(agents)`: drop Anthropic thinking blocks on replay
    - Discord gateway metadata fetch failure handling
    - Delivery dedupe review follow-ups
  - **Assessment:** We're current (npm 2026.3.13 = latest npm). The GitHub tag was just a recovery tag. No action required.

### Documentation (clawddocs)
- clawddocs skill not installed at expected path (`~/.openclaw/workspace/skills/clawddocs`). Scripts skipped.

### ClawHub & Skills
- `clawhub search new` returned news-aggregator skills only — nothing relevant
- `clawhub updates` — no updates available for installed skills
- Installed skills: `web-monitor 1.0.0`, `capability-evolver`, `playwright-scraper-skill`

### Config Health (`openclaw doctor`)
- **Loaded:** 10 skills | **Disabled:** 31 | **Errors:** 0
- Telegram: ✅ ok | Slack: ✅ ok
- Agents active: main, forge, scout, sentinel, venture, taskmaster
- Heartbeat interval: 30m (main)
- No warnings. Doctor suggests `openclaw doctor --fix` but nothing urgent.

### Action Items
- None. System healthy, version current.

---
## 2026-03-15 07:45 UTC — Daily Monitor

### Version
- **Running:** 2026.3.13 (61d171a)
- **Latest GitHub release:** v2026.3.13-1 (recovery tag, 2026-03-14)
  - This is a GitHub tag-only recovery release; npm version remains `2026.3.13`
  - **We are current — no update needed**
- Notable fixes in this release:
  - `fix(telegram)`: thread media transport policy into SSRF (security-adjacent)
  - `fix(compaction)`: full-session token count for post-compaction sanity check
  - `fix(agents)`: drop Anthropic thinking blocks on replay
  - `fix(session)`: preserve lastAccountId and lastThreadId on session reset

### Documentation (clawddocs)
- Skill not installed at expected path (`~/.openclaw/workspace/skills/clawddocs`) — skipped

### ClawHub & Skills
- Installed: `web-monitor` v1.0.0 (only installed skill)
- `clawhub search new` results: news-related skills dominating (cctv-news-fetcher, news, ai-news-oracle, etc.) — nothing relevant to installed skills
- No updates flagged for web-monitor

### Dashboard & UI
- No search performed (nothing flagged as needed)

### Config Health (`openclaw doctor`)
- ✅ No errors
- Loaded: 10 skills, Disabled: 31, Errors: 0
- Telegram: ok | Slack: ok
- Agents: main, forge, scout, sentinel, venture, taskmaster
- Session store: 147 entries — healthy
- No warnings requiring action

### Action Items
- None — system healthy and on current version

---

## 2026-03-16 07:45 UTC — Daily Monitor

### 1. Version Check
- Installed: OpenClaw 2026.3.13 (61d171a)
- Latest on GitHub: v2026.3.13-1 (recovery release, published 2026-03-14)
  - Note: npm package is still 2026.3.13 — the -1 suffix is Git tag/GitHub release only
  - This is a RECOVERY release fixing a broken v2026.3.13 tag path — not a new version
- Status: ✅ UP TO DATE (no action needed)

### Key fixes in v2026.3.13 (recovery):
- fix(compaction): full-session token count for post-compaction sanity check
- fix(telegram): thread media transport policy into SSRF (security)
- fix(session): preserve lastAccountId and lastThreadId on session reset
- fix(agents): drop Anthropic thinking blocks on replay
- fix: address delivery dedupe review follow-ups
- fix: handle Discord gateway metadata fetch failures

### 2. Documentation Changes
- clawddocs skill NOT installed (skills/clawddocs missing) — skipped
- Only 3 skills installed: capability-evolver, playwright-scraper-skill, web-monitor

### 3. ClawHub & Skills
- Top "new" results: news-related skills (new-visitor-cold-start, cctv-news-fetcher, etc.)
- No security-relevant new skills flagged
- Installed skills: capability-evolver, playwright-scraper-skill, web-monitor — no updates checked

### 4. Dashboard & UI
- Not checked (no search results fetched this run)

### 5. Config Health (openclaw doctor)
- Loaded: 10 plugins, Disabled: 31, Errors: 0
- Telegram: ok, Slack: ok
- Agents: main, forge, scout, sentinel, venture, taskmaster
- Session store: 138 entries — healthy
- No errors or warnings requiring action

### Action Items
- The telegram SSRF fix in v2026.3.13 is worth noting but already installed
- clawddocs skill missing — cannot track doc changes until installed
- Consider: `clawhub install clawddocs` if doc monitoring is desired


## 2026-03-18 07:45 UTC — Daily Monitor

### Version Check
- **Installed:** OpenClaw 2026.3.13 (61d171a)
- **Latest on GitHub:** v2026.3.13-1 (recovery release, published 14 Mar)
  - This is a tag/GitHub-only suffix; npm version remains `2026.3.13` — **no update needed**
  - Release notes: bug fix release with multiple fixes across compaction, Telegram SSRF, Discord gateway, session reset, Android UI, iOS onboarding, and agent compatibility

### Documentation
- `~/.openclaw/workspace/skills/clawddocs` directory not found — clawddocs skill not installed locally

### ClawHub & Skills
- **clawhub CLI:** v0.7.0
- **Installed workspace skills:** capability-evolver, playwright-scraper-skill, web-monitor
- `clawhub list` shows only `web-monitor 1.0.0` (working dir context)
- `clawhub updates` / `clawhub check` subcommands not supported in this CLI version
- Notable new skills on ClawHub search (top results): cctv-news-fetcher, news aggregators (not security-relevant)

### Config Health (`openclaw doctor`)
- Telegram: ✅ ok
- Slack: ✅ ok
- Loaded: 10 plugins, Disabled: 31, Errors: 0
- Agents: main, forge, scout, sentinel, venture, taskmaster
- No warnings or errors — clean bill of health

### Action Items
- None urgent. Current version is effectively up to date (2026.3.13 = latest npm)
- Noteworthy fix in latest release: `fix(telegram): thread media transport policy into SSRF` — security-relevant but already included in installed version
- clawddocs skill missing locally (not installed) — no impact unless docs tracking needed


## 2026-03-19 07:45 UTC — Daily Monitor Run

### Version Check
- **Installed:** 2026.3.13 (61d171a)
- **Latest on GitHub:** 2026.3.13 / 2026.3.13-1 (recovery tag, same npm version)
- **Status: UP TO DATE** ✅
- Latest release (2026.3.13) is a recovery release for a broken tag. No new version.
- Notable fixes in current version:
  - fix(compaction): full-session token count for post-compaction sanity check
  - fix(telegram): thread media transport policy into SSRF (security-related)
  - fix(session): preserve lastAccountId and lastThreadId on session reset
  - fix(agents): drop Anthropic thinking blocks on replay
  - feat(android): chat settings UI redesign

### Documentation / clawddocs
- clawddocs skill NOT installed at expected path (~/.openclaw/workspace/skills/clawddocs)
- Skipped doc checks

### ClawHub & Skills
- clawhub search returned news-aggregator type skills (no OpenClaw-core skills in top results)
- No critical security-relevant skill updates identified

### Config Health (openclaw doctor)
- Loaded: 10 plugins/integrations
- Disabled: 31
- Errors: 0 ✅
- Telegram: ok | Slack: ok
- Agents active: main, forge, scout, sentinel, venture, taskmaster
- Sessions store healthy (143 entries)
- Suggestion: "openclaw doctor --fix" available (non-critical)

### Action Items
- None urgent. System healthy.
- clawddocs skill missing — if doc monitoring is desired, reinstall from ClawHub.


---
## 2026-03-20 07:45 UTC — Daily Monitor Run

### Version
- **Installed:** 2026.3.13 (61d171a)
- **Latest on GitHub:** v2026.3.13-1 (recovery release, 14 Mar)
  - This is a Git tag/release-only bump; npm package is still 2026.3.13 — no action needed.

### Release Highlights (v2026.3.13-1 recovery)
- **Bug fixes (no security flags):**
  - `fix(compaction)`: full-session token count for post-compaction sanity check
  - `fix(telegram)`: thread media transport policy into SSRF (#44639) — minor SSRF path fix
  - `fix(session)`: preserve lastAccountId and lastThreadId on session reset
  - `fix(agents)`: drop Anthropic thinking blocks on replay
  - `fix`: Discord gateway metadata fetch failures handled gracefully
  - `fix`: delivery dedupe review follow-ups
- **Misc:** CLI xhigh thinking help text alignment, docs fixes

### Documentation (clawddocs)
- clawddocs skill not installed at expected path — scripts skipped

### ClawHub — New Skills
Top new listings (by score): new-sloth, cctv-news-fetcher, news, hot-news-aggregator, apple-news, ai-news — all news-aggregator type, nothing security-relevant or immediately useful.

### Config Health (openclaw doctor)
- Loaded: 10 plugins, Disabled: 31, **Errors: 0**
- Telegram: ok, Slack: ok
- Agents active: main, forge, scout, sentinel, venture, taskmaster
- Heartbeat: 30m (main)
- No warnings. Clean bill of health.

### Action Items
- None required. Running current npm version. No security releases. Config healthy.

---
## 2026-03-21 07:45 UTC — Daily OpenClaw Monitor

### 1. Version Check
- **Installed:** OpenClaw 2026.3.13 (61d171a)
- **Latest on GitHub:** v2026.3.13 (released 14 Mar) — same version, up to date ✅
- Recovery release `v2026.3.13-1` exists only for GitHub tag purposes; npm version remains `2026.3.13`
- Notable changes in this release:
  - **Bug (session):** `fix(compaction)` — full-session token count for post-compaction sanity check
  - **Security (telegram):** `fix(telegram)` — thread media transport policy into SSRF (Telegram SSRF fix)
  - **Bug (discord):** Handle Discord gateway metadata fetch failures
  - **Bug (session):** Preserve `lastAccountId` and `lastThreadId` on session reset
  - **Bug (agents):** Drop Anthropic thinking blocks on replay
  - **Fix:** Address delivery dedupe review follow-ups
  - **Misc:** CLI xhigh thinking help text alignment, docs fixes

### 2. Documentation / clawddocs
- ⚠️ `clawddocs` skill not installed at expected path (`~/.openclaw/workspace/skills/clawddocs`) — skip

### 3. ClawHub & Skills
- Only 3 skills installed locally: `capability-evolver`, `playwright-scraper-skill`, `web-monitor`
- New trending skills on ClawHub (top by relevance score): news aggregators (cctv-news-fetcher, hot-news-aggregator, apple-news, ai-news, etc.)
- No security-flagged skills noted in new listings

### 4. Dashboard & UI
- No new search performed this cycle (low priority, no notable signals from other checks)

### 5. Config Health (openclaw doctor)
- **Status: Clean ✅** — 0 errors, 10 skills loaded, 31 disabled
- Telegram: ok (@miniClawMTA_bot)
- Slack: ok
- Agents configured: main, forge, scout, sentinel, venture, taskmaster
- Heartbeat: 30m on main
- No warnings; `--fix` flag available but no issues to fix

### Summary
No action needed. System is on latest version. One notable security fix in current version (Telegram SSRF) — already on this version so covered. Config healthy.

---
## 2026-03-22 07:45 UTC

### 1. Version Check
- **Installed:** 2026.3.13 (61d171a)
- **Latest on GitHub:** v2026.3.13-1 (recovery release, 14 Mar)
  - The -1 suffix is GitHub tag only; npm version is still 2026.3.13 — **we are current**
  - Notable fixes in current release:
    - fix(compaction): full-session token count for post-compaction sanity check
    - fix(telegram): thread media transport policy into SSRF ← security-relevant (already on this)
    - fix(session): preserve lastAccountId and lastThreadId on session reset
    - fix(agents): drop Anthropic thinking blocks on replay
    - feat(android): redesign chat settings UI
- **Action needed:** None — on latest

### 2. Documentation (clawddocs)
- clawddocs skill directory not found at expected path (~/.openclaw/workspace/skills/clawddocs)
- Skipped doc tracking scripts

### 3. ClawHub & Skills
- Top new skills on ClawHub: new-sloth, cctv-news-fetcher, news, hot-news-aggregator, apple-news, ai-news
- Mostly news aggregator variants — nothing security-relevant or particularly useful for our stack
- No skill updates checked (no `clawhub update --check` available in this context)

### 4. Dashboard & UI
- Not checked this cycle (no new community integrations found in prior searches)

### 5. Config Health (openclaw doctor)
- Loaded: 10 channels | Disabled: 31 | Errors: **0**
- Telegram: ok | Slack: ok
- Agents: main, forge, scout, sentinel, venture, taskmaster
- Heartbeat: 30m on main
- No warnings; all healthy

### Summary
System healthy. On latest version. No action needed. Config clean with zero errors.

## 2026-03-23 07:45 UTC — Daily Monitor

### Version
- **Current:** OpenClaw 2026.3.13 (61d171a)
- **Latest on GitHub:** v2026.3.13-1 (recovery release, 14 Mar)
  - The -1 suffix is GitHub tag/release only; npm package is still 2026.3.13
  - **We are up to date** (running the same npm version)
- Notable fixes in v2026.3.13:
  - fix(telegram): thread media transport policy into SSRF (#44639)
  - fix(compaction): full-session token count for post-compaction sanity check
  - fix(session): preserve lastAccountId and lastThreadId on session reset
  - fix(agents): drop Anthropic thinking blocks on replay
  - feat(android): redesign chat settings UI

### Documentation (clawddocs)
- clawddocs skill directory not present at expected path (~/.openclaw/workspace/skills/clawddocs)
- Skipped doc tracking scripts

### ClawHub & Skills
- Installed skills: web-monitor 1.0.0, moss 1.0.3
- No update check available via clawhub CLI
- Top new skills on ClawHub: new-house, cctv-news-fetcher, news, news-aggregator, ai-news-oracle (all news/content focused — low relevance)

### Config Health (openclaw doctor)
- ✅ No errors
- Loaded: 10 plugins, Disabled: 31, Errors: 0
- Telegram: ok, Slack: ok
- Agents: main, forge, scout, sentinel, venture, taskmaster
- Session store: 104 entries, active within last 43 min
- No warnings requiring action

### Actions Required
- None. System healthy, version current.

## 2026-03-24 07:45 UTC

### Version
- Installed: 2026.3.13
- Latest: 2026.3.23-2 (**UPDATE AVAILABLE**)

### Release Notes (2026.3.23)
**Changes:**
- ModelStudio/Qwen: added standard DashScope endpoints for China + global Qwen API keys
- UI: consolidated button primitives, Knot theme black-and-red palette (WCAG 2.1 AA), accessibility improvements
- CSP/Control UI: SHA-256 hashes for inline scripts in index.html (security hardening)

**Fixes:**
- Plugins: bundled plugin runtimes (WhatsApp, Matrix, etc.) missing from npm package — now shipped again
- CLI/channel auth: hardened channel IDs against prototype-chain + control-character abuse (SECURITY FIX)
- Auth/OpenAI tokens: live gateway auth writes no longer revert freshly saved credentials to stale in-memory values

### Config Health
- Doctor: clean (0 errors, 10 skills loaded, 31 disabled)
- Telegram: ok | Slack: ok
- Note: "openclaw doctor --fix" available if needed

### ClawHub New Skills (top results)
- recipe-copy-sheet-for-new-month (3.130), new-house (3.107), cctv-news-fetcher (2.361), news (2.317)
- Nothing security-relevant or game-changing in new listings

### Action
- Notify user: new version with security fix in channel auth hardening
