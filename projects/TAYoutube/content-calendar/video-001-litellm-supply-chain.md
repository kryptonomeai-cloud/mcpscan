# Video Script: "This AI Package Was Just Compromised — Your API Keys Are Gone"

**Date:** 2026-03-24 (FILM ASAP — time-sensitive)
**Pillar:** Security + AI crossover
**Target length:** 10-12 minutes
**Primary keyword:** "litellm supply chain attack", "python package malware"
**Thumbnail concept:** Your face (shocked) + padlock breaking apart + "YOUR API KEYS ARE GONE" in red text

---

## Why This Video FIRST

- Discovered TODAY (March 24, 2026) — 433 upvotes on HN within hours
- LiteLLM has 18K+ GitHub stars — massive install base
- Perfectly bridges AI + Security (your two biggest pillars)
- You can actually DEMO the attack safely (download and inspect the wheel)
- Timely + evergreen combo: the attack is news NOW, but supply chain security is forever relevant

---

## Hook (0-15 seconds)

> *[Face cam, serious expression, leaning in]*
> 
> "If you've installed LiteLLM in the last 24 hours... your SSH keys, your API keys, your cloud credentials — all of them — have already been sent to an attacker. And here's the terrifying part: you didn't even have to import it."
>
> *[Cut to terminal showing the malicious .pth file]*

---

## Context (15-60 seconds)

> "LiteLLM is one of the most popular AI proxy libraries — 18,000 stars on GitHub. Thousands of developers use it to route requests to OpenAI, Anthropic, all the big AI providers. Yesterday, versions 1.82.7 and 1.82.8 on PyPI were compromised with a credential stealer. And the way they did it is genuinely clever — and genuinely scary."
>
> *[Show LiteLLM GitHub page, star count, PyPI page]*

---

## The Build / Breakdown

### Step 1: What Happened — The .pth Trick (2 min)
**Screen:** Terminal, downloading the malicious wheel (DO THIS IN AN ISOLATED VM/CONTAINER)
**Say:**
- "The attacker didn't modify any Python source code. They injected a `.pth` file."
- "Here's the thing most devs don't know: `.pth` files in your site-packages get executed AUTOMATICALLY when Python starts. Not when you import. Just... when Python runs."
- "So the moment you installed this package — even if you never imported it — the payload fires."

**Demo:**
```bash
# IN A DISPOSABLE CONTAINER ONLY
pip download litellm==1.82.8 --no-deps -d /tmp/check
# Show the .pth file extraction
# Show the base64-encoded payload
```

**B-roll:** Close-up of terminal, highlight the .pth file

### Step 2: What It Steals — The Full List (2 min)
**Screen:** Scrolling list of targeted files, organised by category
**Say:**
- "Let me show you everything this payload goes after."
- Walk through the categories: SSH keys, git credentials, AWS/GCP/Azure, Kubernetes, Docker, crypto wallets, shell history, CI/CD secrets
- "That's not a credential stealer. That's a credential vacuum cleaner."
- "And here's the brutal part — it grabs your ENTIRE `printenv` output. Every environment variable. Every API key you've ever set."

**Visual:** Animated checklist ticking off each category, getting more alarming

### Step 3: How It Exfiltrates (1.5 min)
**Screen:** Diagram of the encryption + exfil flow
**Say:**
- "They didn't just curl your data raw. They generate a random AES-256 key, encrypt everything, then encrypt the AES key with a hardcoded RSA public key."
- "So only the attacker's private key can decrypt the stolen data. Even if you intercept the traffic, you can't see what was taken."
- "It's sent to `models.litellm.cloud` — notice that's `.cloud`, not `.ai`. The official LiteLLM domain is `.ai`. Classic typosquatting."

**Visual:** Simple diagram: Victim → Encrypt → Exfil → Attacker's Server

### Step 4: How To Check If You're Affected (1.5 min)
**Screen:** Terminal with remediation commands
**Say:**
- "Here's how to check right now."
- Show: `pip show litellm` — check version
- Show: `find / -name "litellm_init.pth" 2>/dev/null`
- Show: Check CI/CD pipeline logs for litellm 1.82.7 or 1.82.8
- "If you find it: you need to rotate EVERYTHING. SSH keys, API keys, cloud credentials, database passwords. All of it. Assume it's all compromised."

### Step 5: The Bigger Picture — Supply Chain Is Broken (2 min)
**Screen:** Face cam, with timeline graphic of recent supply chain attacks
**Say:**
- "This is the third major supply chain attack this month. Trivy got hit. tj-actions/changed-files on GitHub Actions got hit. Now LiteLLM."
- "The AI ecosystem is particularly vulnerable because: everyone `pip installs` random packages, most AI developers are NOT security people, and these packages run with full system access."
- "The Python `.pth` trick is especially nasty because security tools don't scan for it. Your linter won't catch it. Your code review won't catch it. It's not in any `.py` file."

**Visual:** Timeline graphic: Trivy → tj-actions → LiteLLM → ???

### Step 6: How To Protect Yourself (1.5 min)
**Screen:** Terminal + checklist
**Say:**
- "Five things you should do TODAY:"
1. Pin your dependencies — `litellm==1.82.6`, not `litellm>=1.82`
2. Use `pip install --require-hashes` in production
3. Run installs in isolated environments (Docker, VMs)
4. Monitor for .pth files: `find $(python -m site --user-site) -name "*.pth"`
5. Watch for unusual outbound network traffic from your dev machine
- "And honestly? Maybe stop running `pip install` on your main machine. Use virtual environments. Always."

---

## The Payoff (30 seconds)

> *[Face cam]*
> "This attack was discovered today. The packages are still being investigated. If you use LiteLLM in production — and a LOT of AI companies do — check your systems right now. Don't wait for the morning standup."

---

## Outro (15 seconds)

> "I'll be covering more supply chain security and AI security content on this channel. If you want to know when the next big attack drops before it hits your pipeline, subscribe. I'll see you in the next one."

---

## Shorts Opportunities

1. [ ] "This Python trick steals ALL your credentials" — 45 sec: just the .pth file trick explanation
2. [ ] "Everything this malware steals from your computer" — 30 sec: rapid-fire scrolling list
3. [ ] "How to check if you're compromised" — 60 sec: the 3 terminal commands
4. [ ] "3 supply chain attacks in ONE month" — 30 sec: timeline + scale

---

## Technical Requirements

- [ ] Disposable Docker container or VM for safely inspecting the malicious wheel
- [ ] Screen recording of terminal (OBS)
- [ ] Simple diagrams: encryption flow, attack timeline
- [ ] LiteLLM GitHub page screenshot
- [ ] Face cam for hook + context + outro

## SEO Tags
litellm, supply chain attack, python malware, pip security, pypi compromise, credential stealer, ai security, litellm malware, python package security, cybersecurity 2026, open source security, pth file attack, pip install danger, developer security

---

## Notes

- DO NOT show the actual base64 payload decoded on screen (operational security)
- DO show the .pth file trigger mechanism (educational)  
- Mention MCPScan briefly if natural ("I build security tools for AI infrastructure — this is exactly why")
- Cross-reference: Trivy compromise (if you've already covered it, link to that video)
- This video positions you as THE AI security creator — it's worth getting right
