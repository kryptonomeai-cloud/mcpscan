# Video Script: "My AI Assistant Controls My Entire Life (I Built It Myself)"

**Date:** Week 3
**Pillar:** AI
**Target length:** 12-15 minutes
**Primary keyword:** "AI assistant homelab", "personal AI agent", "self hosted AI assistant"
**Thumbnail concept:** Your face (amazed) + phone showing Telegram conversation with JARVIS + robot/AI graphic + "IT RUNS MY LIFE" in text

---

## Hook (0-15 seconds)

> *[Phone screen: Telegram message from JARVIS with a morning briefing]*
> "Every morning at 8 AM, my AI assistant sends me a briefing — weather, emails, calendar, crypto prices, security alerts. It manages my cron jobs, monitors my servers, researches topics while I sleep, and it's running entirely on my own hardware. I built it. Let me show you how."

---

## Context (30 seconds)

> "Everyone's building AI wrappers and chatbots. I built something different — a persistent AI agent that lives on my servers, has access to my tools, remembers our conversations, and proactively does things without me asking. It's like Jarvis, but real. And open source."

---

## The Build

### Segment 1: The Demo (3 min)
**Screen:** Phone + desktop showing Telegram
- Show the morning briefing (real one)
- Ask it to check server status — watch it SSH in and report back
- Ask it to research a topic — watch it search, summarise, save to memory
- Show it running a cron job autonomously
- "It's not just answering questions. It's doing work."

### Segment 2: The Architecture (2 min)
**Screen:** Diagram
- OpenClaw gateway running on a Dell OptiPlex
- Connected to Telegram for messaging
- SSH access to GPU server, NAS, other machines
- CrowdSec for security, SearXNG for search
- Memory system: daily notes + long-term memory file
- Cron jobs: 20+ automated tasks running daily

### Segment 3: What It Does Daily — Without Being Asked (3 min)
**Screen:** Examples of each
- **Morning briefing:** Weather, emails, calendar, crypto, security
- **Security monitoring:** CrowdSec alerts, suspicious activity
- **Server health:** Docker containers, disk space, GPU status  
- **Research:** Scans for new AI papers, tools, security threats
- **Git sync:** Commits and pushes its own workspace changes
- **Backup verification:** Checks backup integrity daily
- Show the cron job list: 20+ jobs all running on schedule

### Segment 4: The Memory System (2 min)
**Screen:** Memory files
- "AI agents forget everything between conversations. Mine doesn't."
- Show MEMORY.md (long-term curated memory)
- Show daily notes (memory/YYYY-MM-DD.md)
- Show SOUL.md (its personality)
- "It remembers decisions, preferences, project context. When I pick up a conversation, it knows where we left off."

### Segment 5: Building Your Own (2 min)
**Screen:** Setup steps (high level — save deep dive for another video)
- OpenClaw: the framework
- Choose your LLM (local or API)
- Connect a messaging channel (Telegram, Discord, Slack)
- Add tools: SSH, web search, cron jobs
- Define personality in SOUL.md
- "You can have this running in under an hour."

---

## Payoff (30 seconds)

> *[Montage: morning briefing, security alert, research summary, server check — all from the AI]*
> "This isn't a chatbot. It's a genuine AI assistant that works 24/7, remembers everything, and keeps getting better. And it costs me nothing beyond electricity."

---

## Outro

> "Want to build your own? I'll do a full step-by-step tutorial next. Subscribe and I'll walk you through the entire setup."

---

## Shorts

1. [ ] "My AI sends me this every morning" — 30 sec: show briefing
2. [ ] "This AI assistant remembers EVERYTHING" — 45 sec: memory system
3. [ ] "I built my own Jarvis" — 60 sec: montage of capabilities
4. [ ] "20 AI cron jobs running while I sleep" — 30 sec: cron list scroll

## SEO Tags
ai assistant, personal ai, self hosted ai assistant, jarvis ai, openclaw, ai agent homelab, telegram ai bot, autonomous ai agent, local ai assistant, ai cron jobs
