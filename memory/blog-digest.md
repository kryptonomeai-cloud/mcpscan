
---

## 2026-03-22 (Sunday 07:15 UTC)

### 🚨 Security (Urgent)

- **FBI Warns: Russian Hackers Target Signal & WhatsApp** — Phishing campaigns targeting encrypted messaging apps; users should enable link-preview warnings and verify QR codes carefully. [Hacker News]
- **⚠️ Oracle patches CVE-2026-21992** — Critical unauthenticated RCE in Oracle Identity Manager. Patch immediately if you run OIM. [Hacker News]
- **⚠️ Trivy Supply Chain Attack / CanisterWorm** — Self-spreading worm hit 47 npm packages via a compromised Trivy scanner update. If you use Trivy in CI, audit your pipeline and lock to a known-good version. [Hacker News]
- **CISA KEV Update: Apple, Craft CMS, Laravel bugs** — Must-patch by April 3, 2026 for federal systems; good practice to patch now regardless. [Hacker News]
- **Cloudflare flags archive.today as C&C/Botnet** — 1.1.1.2 (family-safe DNS) now blocks the archiving site — likely a false positive, but worth noting if you rely on archive.today links. [HN]

### 🤖 AI/ML

- **Simon Willison: Using Git with coding agents** — Practical guide on version control patterns for agentic workflows — commits as checkpoints, branching strategies. Directly relevant for coding agent usage. [Simon Willison]
- **Sashiko: Agentic Linux kernel code review** — AI system autonomously reviewing Linux kernel patches; interesting signal for where agentic code review is heading. [HN]
- **Tinybox — Offline AI device, 120B parameters** — Tinygrad's local inference box supporting 120B-param models offline. Notable hardware milestone. [HN]
- **Thinking Fast, Slow, and Artificial** — Academic paper on how AI is reshaping human reasoning patterns; cognitive offloading concerns. [HN]

### 🛠️ General Tech

- **Simon Willison: Profiling HN users from comments** — Neat LLM-based analysis of comment patterns; interesting demo of text profiling at scale. [Simon Willison]
- **The Three Pillars of JavaScript Bloat** — Solid breakdown of why JS bundles stay fat (framework overhead, polyfills, tree-shaking failures). Good reference for web perf work. [HN]
- **Floci — Free open-source local AWS emulator** — Alternative to LocalStack; worth watching if you do AWS dev locally. [HN]
- **Grafeo — Embeddable graph database in Rust** — Fast, lean graph DB; interesting for anyone needing embedded graph storage. [HN]
- **Professional video editing in browser (WebGPU/WASM)** — Tooscut.app — browser-native pro video editing; WebGPU maturing fast. [HN]
- **Atomic — Self-hosted semantic personal knowledge base** — Show HN; semantically connected notes, self-hosted. Interesting for PKM setups. [HN]
- **Hide macOS Tahoe menu icons** — Quick tip for decluttering the menu bar on macOS Tahoe. [HN]

### ⏭️ Skipped (fluff/off-topic)
Rat King (Wikipedia), Alpha Micro AM-1000E (retro hardware), Chest Fridge (2009), Common Lisp tooling, Termcraft (terminal game), Child protection/internet access op-ed, How Ford burned $12B in Brazil, Boomloom, Some things just take time.

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


## 2026-03-18 — Wednesday Morning Scan (07:15 UTC)

33 new articles found across: Ars Technica AI, Hacker News, OpenAI, Simon Willison, The Hacker News

---

### 🚨 URGENT / FLAG

**[CVE-2026-32746] Critical Telnetd RCE — Unauthenticated Root via Port 23**
Unpatched flaw in telnetd allows unauthenticated root code execution. If anything on your network exposes port 23, kill it now.
→ https://thehackernews.com/2026/03/critical-telnetd-flaw-cve-2026-32746.html

**Apple WebKit Same-Origin Policy Bypass (iOS & macOS) — Patched**
Apple pushed a fix for a WebKit vuln that let attackers bypass SOP; update iOS/macOS promptly.
→ https://thehackernews.com/2026/03/apple-fixes-webkit-vulnerability.html

---

### 🤖 AI / ML

**OpenAI releases GPT-5.4 mini and nano**
Two new lightweight models — nano is extremely cheap (Simon Willison clocks ~76,000 image descriptions for $52). Good for high-volume, cost-sensitive pipelines.
→ https://openai.com/index/introducing-gpt-5-4-mini-and-nano
→ Simon's take: https://simonwillison.net/2026/Mar/17/mini-and-nano/

**Mistral AI Releases Forge**
Mistral's new product launch — details TBC, but worth watching given their cadence.
→ https://mistral.ai/news/forge

**AI Flaws in Amazon Bedrock, LangSmith, SGLang — Data Exfiltration & RCE**
Security researchers found exploitable flaws across three major AI infra platforms. Relevant if using any of these in production.
→ https://thehackernews.com/2026/03/ai-flaws-in-amazon-bedrock-langsmith.html

**"Why AI systems don't learn" — Arxiv paper on autonomous learning from cognitive science**
Academic take on why current AI lacks genuine autonomous learning; useful context for AI capability debates.
→ https://arxiv.org/abs/2603.15381

**Unsloth Studio**
Unsloth launched a Studio UI — model fine-tuning getting more accessible.
→ https://unsloth.ai/docs/new/studio

**Simon Willison: Subagents (Agentic Engineering Patterns)**
Simon's guide on subagent patterns — directly relevant to OpenClaw's own agentic architecture.
→ https://simonwillison.net/guides/agentic-engineering-patterns/subagents/

**Launch an autonomous AI agent with sandboxed execution in 2 lines of code**
onprem library demo — local agent with sandbox; lightweight alternative to heavier frameworks.
→ https://amaiya.github.io/onprem/examples_agent.html

**Get Shit Done: meta-prompting + spec-driven dev system**
GitHub project combining context engineering and spec-driven coding — practical prompting framework.
→ https://github.com/gsd-build/get-shit-done

**CISOs securing AI with yesterday's tools — study**
Survey finds security teams are behind on AI-specific threat models and tooling. No surprise, but worth tracking.
→ https://thehackernews.com/2026/03/ai-is-everywhere-but-cisos-are-still.html

---

### 🔒 Security

**LeakNet Ransomware — ClickFix via hacked sites, Deno in-memory loader**
Novel ransomware chain: compromised sites deliver ClickFix social engineering → in-memory Deno payload. Stealthy and evolving.
→ https://thehackernews.com/2026/03/leaknet-ransomware-uses-clickfix-via.html

**Konni APT — EndRAT via phishing, KakaoTalk for C2 propagation**
North Korea-linked Konni group using KakaoTalk as malware propagation channel alongside phishing.
→ https://thehackernews.com/2026/03/konni-deploys-endrat-through-spear.html

**Microsoft's Xbox One finally hacked via voltage glitching**
'Bliss' hacker broke the "unhackable" 2013 console — voltage glitching allows unsigned code at every level. Impressive exploit, low real-world impact.
→ https://www.tomshardware.com/video-games/console-gaming/microsofts-unhackable-xbox-one-has-been-hacked-by-bliss...

**SSH has no Host header**
Technical deep-dive on SSH's lack of SNI-like host negotiation — relevant for multi-tenant SSH proxying setups.
→ https://blog.exe.dev/ssh-host-header

---

### 🌐 General Tech

**Switzerland built an alternative to BGP**
SCION-based routing deployed nationally — a real-world BGP alternative with path control and fault isolation.
→ https://www.theregister.com/2026/03/17/switzerland_bgp_alternative/

**Python 3.15 JIT back on track**
JIT compiler work for CPython is progressing again after earlier setbacks — relevant for performance-sensitive Python.
→ https://fidget-spinner.github.io/posts/jit-on-track.html

**Edge.js: Node.js apps inside a WebAssembly sandbox (Wasmer)**
Run Node apps in WASM for sandboxed, portable execution — interesting for safe plugin/agent runtimes.
→ https://wasmer.io/posts/edgejs-safe-nodejs-using-wasm-sandbox

**Sub-millisecond VM sandboxes via CoW memory forking (zeroboot)**
Show HN project achieving <1ms sandbox spin-up using copy-on-write forking. Potentially very useful for agent sandbox infra.
→ https://github.com/adammiribyan/zeroboot

**Robotocore — Digital Twin of AWS**
Open-source AWS simulation environment for testing cloud architectures locally. Interesting for dev/test workflows.
→ https://github.com/robotocore/robotocore

---

_Skipped: YC job postings (2), Kita Launch HN, "A Decade of Slug" (retro gaming), product design opinion piece, "Have a Fucking Website" essay, OpenAI compensation tool post, Ars Samsung S26 review_


## 2026-03-19 — Daily Digest

### 🤖 AI/ML

**⚠️ MAJOR: Anthropic — Introducing Claude Opus 4.6**
Anthropic's smartest model gets a significant upgrade. Opus 4.6 is positioned as industry-leading across agentic coding, computer use, tool use, search, and finance — often by wide margins. (Published Feb 5, 2026 — newly indexed today.)

**Google DeepMind — Measuring Progress Toward AGI: A Cognitive Framework**
DeepMind proposes a structured cognitive framework for tracking progress toward AGI, offering a more principled approach than pure benchmark chasing.

**Simon Willison — Autoresearching Apple's "LLM in a Flash" to Run Qwen 397B Locally**
AI auto-research applied to Apple's flash-based LLM inference technique, enabling a 397B parameter model (Qwen) to run locally. Notable for on-device frontier-scale inference.

**Anthropic/HN — What 81,000 People Want from AI**
Anthropic-linked research synthesising what users actually want from AI assistants — useful context for product/design decisions.

**HN — Cook: A Simple CLI for Orchestrating Claude Code**
New open-source tool for orchestrating Claude Code tasks via CLI — could be relevant for agentic workflow automation.

**HN — Machine Payments Protocol (MPP) — Stripe**
Stripe proposes a protocol for machine-to-machine payments, aimed at agentic AI workflows paying for services autonomously. Worth watching as the agent economy matures.

**HN — Nvidia NemoClaw**
NVIDIA releases NemoClaw on GitHub — appears to be an agent/workflow framework. Worth investigating further.

**HN — A Sufficiently Detailed Spec Is Code**
Philosophical but practical post from Haskell For All arguing that detailed enough specs collapse into code — relevant to agentic code generation debates.

---

### 🔐 Security

**🚨 URGENT: Interlock Ransomware — Cisco FMC Zero-Day CVE-2026-20131**
Active ransomware campaign exploiting a Cisco Firepower Management Centre zero-day for root access. Patch/mitigate immediately if running Cisco FMC.

**🚨 URGENT: CVE-2026-3888 — Snap/Ubuntu Local Privilege Escalation to Root**
Critical flaw in snap (systemd cleanup timing exploit) allows local privilege escalation to root on Ubuntu systems. Qualys and THN both flagging it — patch now.

**🚨 URGENT: CISA Warning — Active Zimbra & SharePoint Flaw Exploits**
CISA actively warning of exploitation of Zimbra and SharePoint vulnerabilities alongside the Cisco zero-day ransomware activity.

**🚨 URGENT: 9 Critical IP KVM Flaws — Unauthenticated Root Access (4 Vendors)**
Critical unauth root access vulnerabilities across IP KVM products from 4 vendors. High-value target for infrastructure attackers — check your out-of-band management stack.

**Simon Willison — Snowflake Cortex AI Escapes Sandbox and Executes Malware**
Snowflake's Cortex AI was found to escape its sandbox and execute malicious code. Major prompt/sandbox injection concern for enterprise AI deployments.

**THN — Claude Code Security and Magecart**
Analysis of threat modelling for AI coding agents (Claude Code) in relation to Magecart-style supply chain attacks. Relevant to agentic coding security posture.

**OFAC Sanctions — DPRK IT Worker Network (WMD Funding via Fake Remote Jobs)**
US sanctions a North Korean IT worker network that was funnelling remote job income to WMD programs. Supply chain / hiring risk context.

---

### ⚙️ OpenClaw / Agent Tooling

Nothing direct from the OpenClaw GitHub feed this cycle, but several HN items are relevant:
- **Cook CLI** (Claude Code orchestration) — potentially useful for agentic task pipelines
- **NemoClaw (NVIDIA)** — new agent framework worth watching
- **Machine Payments Protocol** — Stripe's agentic payment layer

---

### 🛠️ General Tech

**Mozilla Firefox 149 — Free Built-in VPN**
Mozilla adding a free built-in VPN to Firefox 149. Privacy-relevant for users; watch for any telemetry implications.

**Ars Technica — Age-Check Tech After Discord Fiasco**
Post-Discord age-verification fallout drives new local-processing age-check tech approaches. Privacy vs. compliance tension ongoing.

**HN — RX: Random-Access JSON Alternative**
New binary-compatible JSON format with random access support — potentially useful for large structured data workloads.

**OpenAI — New Focus on IPO**
Commentary that OpenAI's strategic focus is drifting toward IPO preparation — worth watching for product/API roadmap implications.

---

*33 articles processed. Marked all as read.*

## 2026-03-20 — Daily Digest (07:15 UTC)

### 🚨 URGENT / HIGH PRIORITY

**Security:**
- **DarkSword iOS Exploit Kit** — 6 flaws including 3 zero-days enabling full iPhone takeover; Apple has warned older iPhones are vulnerable. Patch immediately if on older iOS.
- **Azure Sign-In Log Bypass (3rd & 4th)** — TrustedSec discloses two more Azure audit log bypass flaws; attackers can sign in without leaving traces. Major concern for M365-heavy orgs.
- **DoJ Disrupts 3M-Device IoT Botnet** — Botnets behind record 31.4 Tbps DDoS attacks taken down. (Also covered by Krebs.)
- **54 EDR Killers via BYOVD** — 54 malware families exploiting 35 signed vulnerable drivers to disable endpoint security tools. Widespread and serious.
- **FortiGate RaaS + Citrix Exploits** — ThreatsDay bulletin covers active exploitation of FortiGate as ransomware delivery + Citrix vulnerabilities.

---

### 🤖 AI / ML

- **OpenAI acquires Astral** (uv, ruff, ty) — OpenAI buying the Python tooling company behind uv and ruff. Simon Willison has thoughtful commentary on implications for the open-source ecosystem.
- **OpenAI: Monitoring internal coding agents for misalignment** — Blog post on how OpenAI tracks its own AI coding agents for out-of-distribution behaviour. Relevant for anyone deploying agents in production.
- **Scaling Karpathy's Autoresearch with GPU Cluster** — SkyPilot blog on what happens when you give Karpathy's auto-research agent a cluster of GPUs. Interesting scaling dynamics.
- **NanoGPT Slowrun: 10x Data Efficiency** — Research claiming 10x better data efficiency with infinite compute via slower training. Potentially significant if it holds up.
- **Kitten TTS models** — Three new tiny TTS models, smallest under 25MB. Useful for edge/local deployments.
- **Canary (YC W26)** — AI QA tool that understands your codebase for automated quality assurance.
- **Claude Code channels** — Anthropic published docs on pushing events into running Claude sessions via channels. Directly relevant to OpenClaw architecture.

---

### 🔐 Security (non-urgent)

- **Speagle Malware via Cobra DocGuard** — Supply chain attack hijacking document security software to steal data.
- **Perseus Android Banking Malware** — Monitors notes apps to extract sensitive data; targets banking credentials.
- **MCP Abuse in ThreatsDay Bulletin** — MCP (Model Context Protocol) being abused in attacks — worth tracking given OpenClaw's MCP usage.

---

### 🛠️ General Tech

- **Kin: Semantic version control** — Tracks code as entities (functions, classes) rather than files. Interesting rethink of git's model.
- **arXiv declares independence from Cornell** — Preprint server going independent after decades under Cornell. Governance shift for academic publishing.
- **Noq: QUIC implementation in Rust (iroh)** — New QUIC library from the iroh team, relevant for P2P/networking work.
- **Cockpit** — Web-based server management UI trending on HN; solid tool for Linux server admin.
- **Google Android sideloading: 24-hour process** — Google introducing a new 24-hour delay/verification flow for sideloading unverified apps.
- **Clockwise acquired by Salesforce** — AI calendar scheduling tool absorbed into Salesforce.
- **Voltair (YC W26)** — Drone + charging network for power utilities. Infrastructure-scale drone operations.
- **Be intentional about AI and your codebase** — Thoughtful essay on how AI coding tools subtly shift code quality and ownership.

---

*32 articles scanned. 4 urgent security items flagged. All marked as read.*

---

## 2026-03-21 — Morning Digest (07:15 UTC)

27 new articles. Notable items below.

### 🔴 Security — URGENT

**Trivy Security Scanner GitHub Actions Breached — 75 Tags Hijacked**
Critical supply-chain attack: the popular Trivy container scanner's GitHub Actions were compromised, with 75 tags hijacked to steal CI/CD secrets. If you use Trivy in CI, audit your pipelines immediately.
→ https://thehackernews.com/2026/03/trivy-security-scanner-github-actions.html

**CVE-2026-33017 — Critical Langflow Flaw, Exploited Within 20 Hours**
Critical vulnerability in Langflow (popular AI workflow builder) was actively attacked within 20 hours of disclosure. Patch or isolate immediately if running Langflow.
→ https://thehackernews.com/2026/03/critical-langflow-flaw-cve-2026-33017.html

**Magento PolyShell Flaw — Unauthenticated RCE & Account Takeover**
Unauth file upload + RCE + account takeover in Magento. If you run any Magento shops, treat this as urgent.
→ https://thehackernews.com/2026/03/magento-polyshell-flaw-enables.html

**France's Aircraft Carrier Located via Strava — "Stravaleaks"**
Le Monde tracked a French carrier in real time via fitness app data. Classic OPSEC failure resurfacing — relevant reminder if your users have fitness trackers near sensitive locations.
→ https://www.lemonde.fr/en/international/article/2026/03/20/stravaleaks-france-s-aircraft-carrier-located-in-real-time-by-le-monde-through-fitness-app_6751640_4.html

### 🤖 AI/ML

**OpenCode — Open Source AI Coding Agent**
New open-source AI coding agent at opencode.ai. Worth watching as a potential Claude Code / Codex alternative.
→ https://opencode.ai/

**Attention Residuals (MoonshotAI)**
Research from Moonshot AI on attention residuals — architectural ML work, niche but interesting for anyone following transformer internals.
→ https://github.com/MoonshotAI/Attention-Residuals

**Kimi.ai / Cursor integration** (Simon Willison)
Brief note on Kimi.ai and Cursor integration — Moonshot's model appearing in coding tools.
→ https://simonwillison.net/2026/Mar/20/cursor-on-kimi/#atom-everything

**NumKong — 2,000 Mixed Precision Kernels**
Ash Vardanian's library of mixed-precision compute kernels. Interesting for ML infrastructure work.
→ https://ashvardanian.com/posts/numkong/

**ChatGPT Number Bias (7200-7500 range)**
Fascinating finding: ask ChatGPT to pick from 1–10,000 and it consistently clusters around 7200–7500. Neat quirk of LLM training data bias.
→ https://old.reddit.com/r/ChatGPT/comments/1rz2ooh/

### 🔧 General Tech

**Google Adds 24-Hour Wait for Android Sideloading**
Android now enforces a 24h cooling-off period + mandatory reboot for unverified app sideloads. Security win, friction for power users.
→ https://thehackernews.com/2026/03/google-adds-24-hour-wait-for-unverified.html

**Ubuntu 26.04 Ends Silent sudo Passwords**
Ubuntu 26.04 will finally echo asterisks (or similar) when typing sudo passwords — ending 46 years of blank terminal feedback. Small UX change, big muscle-memory adjustment.
→ https://pbxscience.com/ubuntu-26-04-ends-46-years-of-silent-sudo-passwords/

**Rust WASM Parser Rewritten in TypeScript — Got Faster**
Counter-intuitive result: rewriting a Rust/WASM parser in plain TypeScript made it faster. Good reminder that WASM overhead isn't free.
→ https://www.openui.com/blog/rust-wasm-parser

**purl — curl for HTTP Requests Requiring Payment**
New CLI tool for making HTTP requests that require micropayment/authentication flows. Niche but interesting for paid API work.
→ https://www.purl.dev/

**Entso-E Final Report on 2025 Iberian Blackout**
Official post-mortem on the massive April 2025 Iberian power blackout. Infrastructure nerds: required reading.
→ https://www.entsoe.eu/publications/blackout/28-april-2025-iberian-blackout/

### ⏭️ Skipped (fluff/low signal)
- FFmpeg 101 (2024 tutorial, not new)
- Linux APIs book (reference material)
- Red Grid Link (Bluetooth team tracker — niche)
- Ghostling (Ghostty org project, unclear scope)
- Fortran Bluesky client (novelty)
- Japanese chopstick etiquette (culture fluff)
- Molly Guard (old sysadmin concept)
- Turbo Pascal 3.02A deconstructed (nostalgia)
- Project Hail Mary linguistics article (culture)
- Behavioral Analytics in AI Attacks (vendor content)
- Delve fake compliance (satire/commentary)
- Windows quality commitment (PR post)


## 2026-03-23 — Monday 07:15 UTC

### 🚨 URGENT — Security

**CVE-2025-32975 (CVSS 10.0) — Quest KACE SMA Active Exploitation**
Active exploitation of a critical (perfect 10) RCE in Quest KACE SMA systems. Patch immediately if running this device management appliance.
Source: The Hacker News

---

### 🤖 AI / ML

**Flash-MoE: Running a 397B Parameter Model on a Laptop**
Project claims to run a 397B MoE model locally on consumer hardware using flash attention tricks. Impressive if it holds up — worth watching.

**Intuitions for Transformer Circuits**
Explainer on mechanistic interpretability / transformer circuit analysis. Useful reading for anyone digging into model internals.

**Reports of Code's Death Are Greatly Exaggerated**
Steve Krouse pushes back on "vibe coding replaces programmers" hype — argues precision/correctness still matters and AI tools amplify rather than replace engineering rigour.

**They're Vibe-Coding Spam Now**
AI-generated spam emails are already flooding inboxes. Practical signal that LLM-assisted spam is a real and growing problem.

**What Young Workers Are Doing to AI-Proof Themselves** (WSJ)
Workers are doubling down on creative, interpersonal, and physical roles. Interesting labour market signal.

---

### 🔒 Security (non-urgent)

**GrapheneOS: No Personal Information Required**
GrapheneOS reaffirms it will remain usable without account/personal data requirements. Good news for privacy-focused users.

---

### 🛠️ General Tech

**MAUI Is Coming to Linux** (via Avalonia preview)
Microsoft's MAUI UI framework getting Linux support via Avalonia — first preview out. Big deal for .NET cross-platform devs.

**The Future of Version Control — Manyana**
Bram Cohen (BitTorrent creator) proposes a new distributed VCS model. Worth a read if you care about git alternatives.

**Migrating the American Express Payment Network, Twice**
Deep post on how Amex migrated critical payment infrastructure — architecture and war stories.

**RollerCoaster Tycoon Optimization Deep Dive**
A look under the hood of RCT's legendary hand-optimised assembly. Classic "gold standard" story revisited.

**Windows Native App Development Is a Mess**
Honest breakdown of the fragmented Win32/WinUI/MAUI/WPF landscape. Validates why cross-platform frameworks keep winning.

**FPGA 3dfx Voodoo with Modern RTL Tools**
Someone reimplemented the Voodoo GPU in FPGA using modern tooling. Fun retrocomputing/hardware project.

**More Common Mistakes in System Architecture Diagrams**
Practical list of diagram anti-patterns. Useful reference.

---

### 📌 Skipped (fluff/noise)

- HN job posts, "You are not your job" opinion piece, NixOS love letter, PC Gamer RSS irony post, knowledge-offline project (no substance visible), systems reading group retrospective (Microsoft internal interest only), "Collaboration Is Bullshit" op-ed.

---
