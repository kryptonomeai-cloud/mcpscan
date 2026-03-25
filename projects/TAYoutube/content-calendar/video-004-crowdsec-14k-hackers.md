# Video Script: "I Blocked 14,000 Hackers With One Tool (CrowdSec)"

**Date:** Week 2
**Pillar:** Security + Homelab
**Target length:** 10-12 minutes
**Primary keyword:** "crowdsec tutorial", "block hackers homelab", "server security"
**Thumbnail concept:** Your face (intense/focused) + CrowdSec dashboard showing ban count + "14,000 BLOCKED" in red

---

## Hook (0-10 seconds)

> *[Screen: CrowdSec dashboard, ban counter ticking up]*
> "In the last month, 14,000 IP addresses tried to break into my servers. Every single one was automatically detected and banned before they could do anything. This is how."

---

## Context (30 seconds)

> "If you have anything on the internet — a server, a NAS, even a Raspberry Pi with SSH open — people are trying to get in RIGHT NOW. Most of them are bots, brute-forcing passwords 24/7. CrowdSec is a free, open-source tool that detects and blocks them automatically. And it gets smarter the more people use it."

---

## The Build

### Step 1: What CrowdSec Actually Is (1.5 min)
**Screen:** Diagram
- "Think of it as a crowd-sourced firewall"
- How it works: parse logs → detect attacks → share with community → everyone benefits
- Difference from fail2ban: community intelligence, modern architecture, API-driven
- Show the CrowdSec Console (online dashboard)

### Step 2: Install in 2 Minutes (2 min)
**Screen:** Terminal on a fresh server
- Docker install (your setup): show docker-compose snippet
- Or native: `curl -s https://install.crowdsec.net | sudo sh`
- Install the firewall bouncer: `sudo apt install crowdsec-firewall-bouncer-iptables`
- "That's it. It's already watching your SSH logs."

### Step 3: See It Working (2 min)
**Screen:** Terminal + dashboard
- `cscli decisions list` — show active bans
- `cscli alerts list` — show detected attacks
- `cscli metrics` — show processed lines, parsed events
- "See that? 14,000 decisions. Each one is an IP that was caught trying something."
- Show the Console dashboard (web UI)

### Step 4: What It Catches (2 min)
**Screen:** Attack examples
- SSH brute force (the most common)
- HTTP vulnerability scans
- Log4Shell probes (still happening in 2026!)
- WordPress exploit attempts
- Show actual log entries being parsed in real-time
- "These aren't hypothetical threats. This is what's hitting YOUR server right now."

### Step 5: Custom Scenarios (1.5 min)
**Screen:** Config files
- Install additional collections: `cscli collections install crowdsecurity/nginx`
- Show available collections for different services
- "Running Docker? There's a collection for that. Nginx? Got it. Traefik? Yep."
- Briefly show how to write a custom scenario (for power users)

### Step 6: The Community Intelligence Angle (1 min)
**Face cam + diagram:**
- "Here's what makes CrowdSec different from fail2ban"
- When you detect an attack, that IP is shared with the community
- Everyone's CrowdSec blocks known-bad IPs before they even try
- "You're not just protecting yourself. You're protecting everyone."

---

## Payoff (30 seconds)

> *[Dashboard showing stats]*
> "Free, open source, 5-minute setup, and it's already caught 14,000 attacks on my network. If you have anything exposed to the internet and you're NOT running this, you're flying blind."

---

## Outro

> "Next time: I'll show you the rest of my security stack — how I monitor, detect, and respond to threats across my entire homelab. Subscribe if you want to sleep better at night."

---

## Shorts

1. [ ] "14,000 hackers tried to break in" — 30 sec: dashboard reveal + stats
2. [ ] "Install this on your server RIGHT NOW" — 45 sec: speed install
3. [ ] "Your server is being attacked right now" — 30 sec: show live brute force attempts
4. [ ] "CrowdSec vs Fail2ban — which is better?" — 60 sec: quick comparison

## SEO Tags
crowdsec, server security, homelab security, block hackers, fail2ban alternative, crowdsec tutorial, linux security, self hosted security, ssh brute force, cybersecurity homelab, crowdsec docker
