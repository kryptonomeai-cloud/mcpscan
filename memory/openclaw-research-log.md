
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
