
---

## 2026-03-15 (Sunday 07:15 UTC)

### 🚨 URGENT / HIGH PRIORITY

**[OpenClaw] OpenClaw AI Agent Flaws Could Enable Prompt Injection and Data Exfiltration** *(The Hacker News)*
China's CNCERT issued a formal warning about OpenClaw's weak default security configs enabling indirect prompt injection (IDPI) attacks. Malicious web pages could cause the agent to leak sensitive data during routine browsing/summarisation tasks. This is you — worth reviewing your skill allowlists and web-fetch exposure.
→ https://thehackernews.com/2026/03/openclaw-ai-agent-flaws-could-enable.html

---

### 🔧 OpenClaw

**[OpenClaw] Release v2026.3.13-1** *(OpenClaw GitHub)*
Recovery release fixing a broken v2026.3.13 tag. Key fixes: post-compaction token count sanity check, Telegram SSRF policy fix for media transport, Discord gateway metadata fetch failure handling, session reset now preserves lastAccountId/lastThreadId.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.3.13-1

---

### 🔐 Security

**[Security] GlassWorm Supply-Chain Attack Abuses 72 Open VSX Extensions** *(The Hacker News)*
A supply-chain campaign compromised 72 VS Code-compatible Open VSX extensions to target developers. If using VSCodium or Open VSX-based editors, audit installed extensions immediately.
→ https://thehackernews.com/2026/03/glassworm-supply-chain-attack-abuses-72.html

---

### 🤖 AI/ML

**[AI] MCP is dead; long live MCP** *(Hacker News)*
Discussion/essay on the evolving state of the Model Context Protocol — likely covers limitations or a successor spec. Worth a read if actively using MCP integrations.
→ https://chrlschn.dev/blog/2026/03/mcp-is-dead-long-live-mcp/

**[AI] Tree Search Distillation for Language Models Using PPO** *(Hacker News)*
Technical post on distilling tree-search reasoning into LLMs via PPO — relevant to agentic reasoning quality improvements.
→ https://ayushtambde.com/blog/tree-search-distillation-for-language-models-using-ppo/

**[AI] Simon Willison — Agentic Engineering at the Pragmatic Summit** *(Simon Willison)*
Fireside chat recap on agentic engineering practices — Simon's takes are usually sharp and practical.
→ https://simonwillison.net/2026/Mar/14/pragmatic-summit/#atom-everything

---

### 💻 General Tech

**[Tech] A Most Elegant TCP Hole Punching Algorithm** *(Hacker News)*
Interesting networking post on peer-to-peer connectivity — potentially relevant to distributed/self-hosted setups.

**[Tech] Postgres with Builtin File Systems** *(Hacker News / db9.ai)*
Postgres variant with native filesystem integration — intriguing for data-heavy deployments.

**[Tech] Fedora 44 on the Raspberry Pi 5** *(Hacker News)*
Practical guide for Pi 5 Fedora setup — relevant if running Pi-based nodes.

**[Tech] How Kernel Anti-Cheats Work** *(Hacker News)*
Deep dive into kernel-level anti-cheat mechanisms — interesting from a security/OS perspective.

*Skipped: rack-mount hydroponics, treasure hunter story, bumblebee biology, Washington Post piece, creative/show HN projects (GrobPaint, Han language, Ichinichi notes app), Ageless Linux, Marketing for Founders, SBCL Fibers, Library of Short Stories, Airbus UCAV news.*


---

## 2026-03-16 (Monday) — 07:15 UTC

### 🤖 AI/ML

- **"What is agentic engineering?"** (Simon Willison + HN) — Simon published a guide to agentic engineering patterns. Likely worth reading for OpenClaw/agent design work. [Link](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/)
- **"How I write software with LLMs"** (HN) — Practical first-person account of LLM-assisted software dev workflow. [Link](https://www.stavros.io/posts/how-i-write-software-with-llms/)
- **"LLMs can be exhausting"** (HN) — Honest take on the fatigue of working with LLMs daily — emotional/ergonomic angle. [Link](https://tomjohnell.com/llms-can-be-absolutely-exhausting/)
- **LLM Architecture Gallery** (HN) — Sebastian Raschka's visual gallery of LLM architectures — handy reference. [Link](https://sebastianraschka.com/llm-architecture-gallery/)
- **Quillx / AIx open standard** (HN) — Proposal for an open standard to disclose AI involvement in software projects (like a `.ai-disclosure` file). [Link](https://github.com/QAInsights/AIx)
- **Athletic humanoid tennis via imperfect motion data** (HN) — DeepMind-style robotics: training humanoid to play tennis from imperfect human motion capture. Neat advance. [Link](https://zzk273.github.io/LATENT/)
- **Stop Sloppypasta** (HN) — Campaign/tool to detect and flag lazy AI copy-paste in code/text. [Link](https://stopsloppypasta.ai/)

### 🔒 Security

- **⚠️ Glassworm Unicode attacks back** (HN) — **FLAG**: Invisible Unicode characters used to inject malicious code into GitHub repos, npm packages, and VSCode extensions. Ongoing active campaign. Relevant for any OSS contributors. [Link](https://www.aikido.dev/blog/glassworm-returns-unicode-attack-github-npm-vscode)
- **Android 17 blocks accessibility API abuse** (The Hacker News) — Android 17 restricts non-accessibility apps from using the Accessibility API, closing a major malware vector. Good news for Android security. [Link](https://thehackernews.com/2026/03/android-17-blocks-non-accessibility.html)
- **Canada Bill C-22 — mass metadata surveillance** (HN) — Canadian legislation mandates warrantless metadata access; significant privacy concerns flagged by Michael Geist. [Link](https://www.michaelgeist.ca/2026/03/a-tale-of-two-bills-lawful-access-returns-with-changes-to-warrantless-access-but-dangerous-backdoor-surveillance-risks-remains/)

### 🛠 General Tech

- **Chrome DevTools MCP** (HN, 2025) — Chrome DevTools now has an MCP server for debugging browser sessions from AI agents. Relevant for browser automation work. [Link](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- **GitHub Actions as PaaS control plane** (HN) — Experiment using GitHub Actions as the orchestration layer for a homebrew PaaS. Creative infra hack. [Link](https://towlion.github.io)
- **Federal Right to Privacy Act draft** (HN) — US draft legislation for a federal privacy law; worth watching if it gains traction. [Link](https://righttoprivacyact.github.io)
- **Separating Wayland compositor & window manager** (HN) — Technical post on River WM's approach to splitting compositor and WM responsibilities. [Link](https://isaacfreund.com/blog/river-window-management/)

### ⏭ Skipped (older/fluff)
- ASCII/Unicode quotation marks (2007 reference post)
- Visual Intro to ML (2015 classic, not new)
- Intel Optane explainer (2023 archive)
- Linux Programming Interface as course text (reference)
- Nasdaq's Shame (finance/market piece, low relevance)
- The 49MB web page (web bloat audit, interesting but low priority)
- Cannabinoids & Alzheimer's (2016 research, surfaced as curiosity)


---

## 2026-03-17 — Daily Blog Digest

### 🤖 AI/ML

**⚠️ Mistral Small 4 Released** (Simon Willison / Mistral)
Huge new open-source model: 119B parameters (MoE, 6B active), Apache 2.0 licensed. Combines reasoning (Magistral), multimodal (Pixtral), and agentic coding (Devstral) in one model. 242GB on HuggingFace. Supports `reasoning_effort` parameter.

**Codex Subagents Now GA** (Simon Willison / OpenAI)
OpenAI Codex subagents out of preview and into general availability. Works similarly to Claude Code's implementation — default agents (explorer, worker, default) plus custom TOML-defined agents in `~/.codex/agents/`. Supports custom models per agent.

**Leanstral: Open-Source Agent for Formal Proof Engineering** (Mistral / HN)
Mistral releases Leanstral, a coding agent built on Lean 4 for formal verification. Aims to reduce human review bottleneck in high-stakes code by formally proving implementations against specs. 6B active params, open-source.

**Coding Agents for Data Analysis** (Simon Willison)
Simon's NICAR 2026 workshop handout — practical guide on using Claude Code and Codex for data journalism (DB queries, data cleaning, visualisations, scraping). Good reference material.

**Anthropic Alignment Quote** (Simon Willison)
Anthropic alignment-science team member on the blackmail exercise: the point was to create visceral, policy-relevant results demonstrating misalignment risk. Referenced in a New Yorker piece on the Pentagon/Anthropic relationship.

**Language Model Teams as Distributed Systems** (HN / arXiv)
Academic paper modelling LLM development teams as distributed systems — potentially interesting lens on coordination and failure modes in AI development orgs.

---

### 🔐 Security

**⚠️ CISA KEV: Wing FTP CVE-2025-47813 Actively Exploited**
CVSS 4.3 — info disclosure leaking server install path via long UID cookie. Affects Wing FTP ≤7.4.3, patched in 7.4.4. CISA confirmed active exploitation. Patch if you run Wing FTP.

**⚠️ GlassWorm Supply Chain Attack: GitHub Tokens → Python Repos**
Stolen GitHub tokens used to force-push malware into hundreds of Python repos (Django apps, ML code, Streamlit dashboards, PyPI packages). Malware appended to `setup.py`, `main.py`, `app.py`. Anyone running `pip install` from a compromised repo is at risk. Injections started ~March 8. Review any recently installed Python packages.

**⚠️ MacSync macOS Infostealer via ClickFix + Fake AI Tool Installers**
Three ClickFix campaigns distributing MacSync infostealer on macOS via fake AI tool installers. Social-engineering based (user runs copied terminal commands). Actively targeting macOS users — be cautious with any "install this AI tool" prompts.

**Weekly Recap: Chrome 0-Days, Router Botnets, AWS Breach, Rogue AI Agents**
Google patched 2 actively exploited Chrome 0-days: CVE-2026-3909 (OOB write in Skia) and a second high-severity bug. Also covered: router botnets, AWS breach, rogue AI agent activity. Busy week.

**DRILLAPP Backdoor Targeting Ukraine via Microsoft Edge Debugging**
State-level espionage tool abusing Edge's remote debugging protocol for stealth. Geopolitically motivated, likely not broadly relevant but notable technique.

**Why Security Validation Is Becoming Agentic** (The Hacker News — sponsored/opinion)
Industry piece on agentic security validation — more signal than ad, worth a skim if evaluating SecOps tooling.

---

### 🛠️ OpenClaw / Tooling

**OpenAI: Why Codex Security Doesn't Include a SAST Report** (OpenAI)
Interesting rationale piece — OpenAI explains their security posture decision for Codex, presumably relevant to how we think about agentic coding tool security.

**Show HN: Claude Code Skills for Godot Game Building** (HN)
Someone built Claude Code skills that generate complete Godot games (godogen). Niche but interesting example of Claude Code skill composition.

**Voygr (YC W26): Maps API for AI Agents** (HN)
New maps API specifically designed for agents and AI apps — potentially useful for location-aware agent workflows.

---

### 💻 General Tech

**Jepsen: MariaDB Galera Cluster 12.1.2** (HN)
New Jepsen distributed systems analysis. If you run MariaDB Galera, worth reading for consistency/correctness findings.

**"Every Layer of Review Makes You 10x Slower"** (HN / apenwarr)
Engineering culture post on review overhead — resonant given the agentic AI velocity context.

**AirPods Max 2** (HN / Apple)
Apple released AirPods Max 2. Incremental upgrade.

**SEC Preparing to Scrap Quarterly Reporting Requirement** (HN / Reuters)
Significant regulatory change — US SEC may drop mandatory quarterly earnings reports. Big deal for public company finance/IR.

**Meta's Renewed Commitment to jemalloc** (HN)
Meta doubling down on jemalloc memory allocator for data infrastructure. Interesting for systems/infra folks.

