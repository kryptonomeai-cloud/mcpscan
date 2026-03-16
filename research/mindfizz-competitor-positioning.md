# MindFizz Competitor Analysis & Market Positioning

*Generated: 14 March 2026*

---

## 1. UK Cybersecurity Market Overview

**Source:** UK Government Cyber Security Sectoral Analysis 2025 (DSIT/Ipsos)

- **2,165 active cyber security firms** in the UK
- **£13.2 billion** annual sector revenue (+12% YoY)
- **£7.8 billion** GVA (+21% YoY)
- **67,300 FTEs** (+6,600 new jobs, +11% YoY)
- **£206 million** raised across 59 deals in 2024
- Half of firms located **outside London/South East** — regional growth strong
- Severe **skills shortage** persists, especially in cloud security, incident response, and AI security

**Key trend:** AI security is emerging as a distinct sub-sector. MCP (Model Context Protocol) security specifically is a brand-new niche with almost no established players — representing a significant first-mover opportunity.

---

## 2. Competitive Landscape

### 2.1 Direct Competitors: MCP Security Tools

These are the closest competitors to MindFizz's MCPScan product.

#### mcp-security-scan (cc-fuyu)
- **URL:** https://github.com/cc-fuyu/mcp-security-scan
- **Type:** Open source CLI tool (npm/npx)
- **Founded:** ~2025-2026
- **License:** MIT
- **What it does:** Scans MCP server config files for vulnerabilities mapped to OWASP MCP Top 10. Auto-discovers configs from Claude Desktop, Cursor, VS Code, Windsurf, Continue.dev, Zed, Cline.
- **Features:** Auth gaps, secret exposure, transport security, SSRF, command injection, permissions, supply chain, tool poisoning detection. JSON/HTML/terminal output.
- **Key stat:** Found 41% of public MCP servers have no authentication
- **Team:** Individual developer / small team
- **Pricing:** Free (MIT)
- **Differentiator vs MindFizz:** npm ecosystem (vs Python), broader IDE config auto-discovery, OWASP MCP Top 10 mapping
- **Weakness:** No consulting services, no enterprise support, no local-first privacy story, no broader security advisory

#### mcpscan.ai
- **URL:** https://mcpscan.ai
- **Type:** Cloud-based SaaS scanner
- **What it does:** Scan GitHub repos containing MCP server implementations for vulnerabilities. Maintains a comprehensive vulnerability taxonomy (command injection, code injection, path traversal, resource exhaustion, IDOR, tool poisoning, rug pulls, cross-server shadowing, indirect prompt injection, data exfiltration, confused deputy attacks, config/env vulnerabilities)
- **Key features:** GitHub repo URL input → automated scan; knowledge base of vulnerability patterns with code examples
- **Pricing:** Unclear (appears free for basic scans)
- **Differentiator vs MindFizz:** Cloud-based (scans remote repos), comprehensive taxonomy documentation
- **Weakness:** Cloud-dependent (data leaves your machine), no local execution, no consulting, no privacy guarantees

#### Vulnerable MCP Project (vulnerablemcp.info)
- **URL:** https://vulnerablemcp.info
- **Type:** Vulnerability database / research project
- **What it does:** Tracks and documents real-world MCP vulnerabilities with CVEs, severity ratings, exploitability assessments
- **Notable findings tracked:** CVEs in MCP TypeScript SDK, MCPJam inspector (RCE, CVSS 9.8), Anthropic's mcp-server-git chain (RCE), SSRF in MarkItDown, path traversal in filesystem-mcp, Zen MCP server path bypass
- **Differentiator:** Pure research/database — not a tool, but an essential reference
- **Relevance:** Potential partnership/citation opportunity for MindFizz

#### ModelContextProtocol-Security.io
- **URL:** https://modelcontextprotocol-security.io
- **Type:** Cloud Security Alliance community project
- **What it does:** Comprehensive security guides, Top 10 risks, hardening guides, audit frameworks, TTPs database, vulnerability tracking
- **Resources:** Why MCP Security, MCP Top 10, Hardening Guide, Build Security, Operational Security, Reference Patterns, Audit & Compliance, Tools & Scripts
- **Differentiator:** Community-driven, backed by CSA, bi-weekly working group meetings
- **Relevance:** Standards body — MindFizz should align with and contribute to this

---

### 2.2 Adjacent Competitors: AI Security Platforms

These companies operate in the broader AI security space and could expand into MCP security.

#### Adversa AI
- **URL:** https://adversa.ai
- **Founded:** ~2019 (Israel-based, not UK)
- **CEO:** Alex Polyakov
- **What they do:** AI security for agents, applications, models, MCP and beyond. Automated red teaming for LLMs, adversarial AI attack research, facial recognition attacks
- **Services:** AI red teaming, guardrail testing, AI agent security, MCP security research (published MCP Top 25 Vulnerabilities)
- **Media presence:** Featured in Fortune, Forbes, TechCrunch, MIT Technology Review, Wall Street Journal, Gizmodo, Vice, Politico, DarkReading
- **Funding:** Venture-backed
- **Target:** Enterprise, government
- **Differentiator vs MindFizz:** Massive media presence, broad AI security (not just MCP), research credibility
- **Weakness:** Not UK-based, enterprise pricing, cloud-based, no open source tools

#### Enkrypt AI
- **URL:** https://www.enkryptai.com
- **Founded:** ~2023 (US-based)
- **What they do:** "World's Most Comprehensive AI Security Platform" — agentic security & compliance
- **Products:** Agent Red Teaming, Agent Guardrails, AI Data Risk Audit, Agent Policy Engine
- **Recognition:** Gartner Cool Vendor in AI Security 2025
- **Claims:** Reduce time to certify by 90%, detect prompt injection, jailbreaking, data leakage, model inversion, adversarial attacks, policy violations
- **Published:** Blog on MCP security vulnerabilities (references MCP Gateway, MCP Scanner, MCP Registry)
- **Target:** Enterprise
- **Differentiator vs MindFizz:** Full platform (not just scanning), Gartner recognition, broader coverage
- **Weakness:** Not UK-based, enterprise pricing, cloud-dependent, no open source

#### SplxAI (SPLX)
- **URL:** https://splx.ai
- **Founded:** 2023 (London-registered, £9M raised)
- **What they do:** End-to-end security for AI — red teaming, runtime protection, governance, remediation
- **Products:** AI Discovery & AI-BOM (discovers models, MCP servers, guardrails across enterprise), Automated Red Teaming, AI Runtime Protection, AI Governance & Compliance, Dynamic Remediation, AI Runtime Threat Inspection, AI Model Security
- **Key feature:** **Explicitly mentions MCP server discovery** in their platform
- **Target:** Enterprise
- **Differentiator vs MindFizz:** Full platform approach, MCP discovery built into broader AI security, enterprise governance
- **Weakness:** Enterprise pricing/complexity, not open source, cloud-dependent

#### Harmonic Security
- **URL:** https://www.harmonicsecurity.com
- **Founded:** 2023 (UK, London-based, £17.5M raised)
- **Founder:** Alastair Paterson (co-founder of Digital Shadows, acquired by ReliaQuest)
- **What they do:** Zero-touch data protection platform for AI — prevents sensitive data from flowing into AI tools
- **Target:** Enterprise
- **Differentiator vs MindFizz:** DLP for AI (different focus — data protection not config scanning)
- **Relevance:** Complementary, not directly competitive. Potential partner.

---

### 2.3 UK Cybersecurity Startups (Traditional — Less Directly Competitive)

| Company | URL | Focus | Target | Relevance to MindFizz |
|---------|-----|-------|--------|----------------------|
| **CybaVerse AI** | cybaverse.co.uk | AI-powered cyber ops platform (CybaOps), MSSP for SMEs | SME/MSP | Low — traditional SOC/MSSP, no AI agent security |
| **OnSecurity** | onsecurity.io | AI-augmented penetration testing, transparent hourly billing | SME/Enterprise | Low — manual pen testing, no MCP/AI agent focus |
| **GoDefend** | godefend.co.uk | CREST-accredited pen testing, continuous monitoring for SMEs | SME | Low — traditional pen testing, no AI security |
| **Cytix** | cytix.io | Continuous AI-powered security testing platform | SME/Enterprise | Medium — AI-powered testing could expand into AI security |
| **Tracebit** | tracebit.com | Security detection & containment, rapid incident response | Enterprise | Low — incident response, not preventive scanning |
| **Melius Cyber** | meliuscyber.com (→ godefend.co.uk) | Cyber risk detection for SMEs (now GoDefend) | SME | Low — traditional cyber risk, merged/rebranded |

---

## 3. MindFizz Unique Value Propositions

Based on the competitive analysis, MindFizz has several clear differentiators:

### 3.1 Open Source + Local-First
- **MCPScan is open source** (vs mcpscan.ai which is cloud-only, vs Enkrypt/SPLX/Adversa which are proprietary SaaS)
- **100% local execution** — zero data leaves the machine. This is a massive selling point for:
  - Financial services firms (regulatory concerns)
  - Government/defence (classified environments)
  - Healthcare (patient data)
  - Any org with strict data sovereignty requirements

### 3.2 Python Ecosystem
- MCPScan is Python-based (pip install) vs cc-fuyu's npm-based scanner
- Python is the lingua franca of security tooling — better fit for security teams' existing toolchains
- Easy integration with CI/CD (GitHub Actions, GitLab CI, Jenkins)

### 3.3 Consulting + Tool (Hybrid Model)
- Most competitors are **either** a tool **or** a consultancy — MindFizz can be both
- Open source tool as lead gen → consulting services for implementation, custom policies, ongoing advisory
- This is the **Red Hat model** applied to AI security

### 3.4 UK-Based
- UK data sovereignty, UK legal jurisdiction
- Aligned with UK Cyber Security & Resilience Bill (forthcoming)
- Eligible for UK government contracts (G-Cloud, DOS)
- Can leverage NCSC alignment and Cyber Essentials pathways

### 3.5 MCP-Specific Expertise
- While Adversa, Enkrypt, and SPLX cover AI security broadly, MindFizz can be **the** MCP security specialist
- Deep expertise > broad coverage for a niche this new
- First-mover advantage in an emerging market segment

---

## 4. Competitive Positioning Matrix

| Capability | MindFizz (MCPScan) | cc-fuyu mcp-security-scan | mcpscan.ai | Adversa AI | Enkrypt AI | SPLX |
|-----------|-------------------|--------------------------|------------|------------|------------|------|
| Open Source | ✅ | ✅ | ❌ | ❌ | ❌ | Partial |
| Local-First (no cloud) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| MCP Config Scanning | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| MCP Server Code Analysis | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| AI Red Teaming | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Runtime Guardrails | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| MCP Discovery (Enterprise) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Consulting Services | ✅ (planned) | ❌ | ❌ | ✅ | ✅ | ✅ |
| UK-Based | ✅ | ❌ | ❌ | ❌ (Israel) | ❌ (US) | ✅ |
| CI/CD Integration | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| OWASP MCP Top 10 | ✅ | ✅ | Partial | ✅ | ❌ | ❌ |
| Enterprise Support | Planned | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pricing | Free + Services | Free | Free/Unknown | Enterprise $$ | Enterprise $$$ | Enterprise $$ |

---

## 5. Target Customer Profile

### Primary: UK SMBs Adopting AI Agents (50-500 employees)
- **Who:** Tech-forward SMBs deploying AI agents (Claude, GPT, Copilot) with MCP integrations
- **Pain:** No security review process for MCP configs, worried about compliance (GDPR, upcoming Cyber Resilience Bill), can't afford enterprise AI security platforms
- **Budget:** £500-5,000/month for security services
- **Decision maker:** CTO, Head of Engineering, CISO (if they have one)
- **Why MindFizz:** Affordable, UK-based, open source tool they can try before buying services

### Secondary: UK Enterprises with AI/ML Teams
- **Who:** Large enterprises (500+) with dedicated AI/ML teams deploying MCP servers
- **Pain:** Need to audit MCP deployments across engineering teams, regulatory compliance pressure, security team lacks AI agent expertise
- **Budget:** £5,000-25,000/month
- **Decision maker:** CISO, VP Engineering, Head of AI
- **Why MindFizz:** Local-first for data sovereignty, consulting for policy development, CI/CD integration

### Tertiary: AI Startups and Platform Companies
- **Who:** Companies building AI agent platforms or MCP server implementations
- **Pain:** Need security validation before shipping, customer trust requirements, potential liability
- **Budget:** Variable (£1,000-10,000/project)
- **Decision maker:** CTO, Security lead
- **Why MindFizz:** Pre-release security audits, ongoing scanning in CI/CD

---

## 6. Pricing Strategy Recommendation

### Tier 1: Free (Open Source MCPScan)
- Full CLI scanner, unlimited local scans
- Community support (GitHub issues)
- CI/CD integration guides
- **Purpose:** Lead generation, community building, brand awareness

### Tier 2: MCPScan Pro — £49/month per org
- Everything in Free, plus:
- Priority email support
- Custom rule definitions
- HTML/PDF report generation with branding
- Dashboard for scan history and trends
- Slack/Teams notifications
- **Purpose:** SMBs wanting ongoing monitoring

### Tier 3: Security Assessment — £2,500-7,500 (one-off)
- Comprehensive MCP security audit
- Review of all MCP server configurations
- AI agent threat modelling
- Written report with prioritised findings and remediation plan
- 1 hour follow-up consultation
- **Purpose:** Project-based revenue, builds relationships

### Tier 4: Managed AI Security — £2,000-8,000/month
- Ongoing MCP security monitoring and advisory
- Monthly security reviews
- Policy development and maintenance
- Incident response support for AI/MCP issues
- Quarterly threat briefings
- **Purpose:** Recurring revenue, high-value client relationships

### Rationale:
- cc-fuyu and mcpscan.ai are free — don't compete on tool price, compete on services
- Enterprise AI security platforms (Enkrypt, SPLX, Adversa) charge £50,000-200,000+/year — massive gap in the market for mid-tier pricing
- UK pen testing firms charge £800-1,500/day — align consulting pricing with this norm

---

## 7. Go-to-Market Recommendations

### Phase 1: Build Credibility (Months 1-3)
1. **Publish MCPScan on PyPI** with comprehensive docs and examples
2. **Write a "State of MCP Security" report** — scan public MCP registries, publish aggregate findings (like cc-fuyu's "41% have no auth" stat)
3. **Contribute to ModelContextProtocol-Security.io** community (CSA project) — join working group, contribute audit findings
4. **Blog series:** "MCP Security for UK Businesses" — SEO play targeting UK-specific queries
5. **Get listed on OWASP MCP resources** as a recommended tool
6. **Submit to Vulnerable MCP Project** — share findings, build relationship

### Phase 2: Generate Leads (Months 3-6)
1. **Launch MCPScan Pro** with self-serve signup
2. **Speak at UK security events:** BSides London, InfoSec Europe, CyberUK (NCSC)
3. **Partner with UK MCP/AI meetups** — offer free security workshops
4. **LinkedIn thought leadership:** "Why your MCP configs are probably leaking secrets" — target UK CTOs/CISOs
5. **Apply for Cyber Essentials certification** for MindFizz itself — table stakes for UK gov work
6. **Offer free security assessments** to 10 notable UK AI startups — case studies and testimonials

### Phase 3: Scale (Months 6-12)
1. **G-Cloud listing** — essential for UK public sector sales
2. **CREST accreditation** for consulting services (or partner with a CREST-accredited firm)
3. **Build partnerships** with AI platform companies (Anthropic, OpenAI ecosystem partners)
4. **Develop training courses:** "Securing AI Agents with MCP" — for developer and security audiences
5. **Explore integration** with SPLX or similar platforms as the MCP scanning engine

---

## 8. Key Messaging vs Each Competitor

### vs cc-fuyu/mcp-security-scan
> "Both open source, but MCPScan is Python-native for security teams, locally installed for air-gapped environments, and backed by expert consulting when you need more than a scan."

### vs mcpscan.ai
> "Your MCP configs contain API keys, internal URLs, and infrastructure details. Why upload them to a cloud service? MCPScan runs 100% locally — your configs never leave your machine."

### vs Adversa AI
> "Adversa is excellent for broad AI red teaming. For MCP-specific security — the actual configurations connecting your agents to your infrastructure — you need a specialist. That's MindFizz."

### vs Enkrypt AI
> "Enterprise AI governance platforms start at six figures. MCPScan gives you MCP security scanning today, for free, with expert consulting when you need it. Start secure, scale smart."

### vs SPLX
> "SPLX discovers your MCP servers. MCPScan secures them. We're complementary — and we're the only tool that runs entirely on your infrastructure."

### vs traditional UK pen testers (OnSecurity, GoDefend, etc.)
> "Your pen tester checks your web apps and networks. Who's checking the AI agents you just connected to your production database via MCP? That's a different attack surface entirely."

---

## 9. Risk Assessment

### Threats
- **SPLX** is the most dangerous competitor — UK-based, well-funded (£9M), already mentions MCP in their platform. Could subsume the MCP scanning niche into their broader platform.
- **Anthropic** could build native MCP security tooling, making third-party scanners less relevant.
- **OWASP/CSA** community projects could produce free comprehensive tools that match MCPScan's functionality.
- **cc-fuyu** could add consulting/support tiers and become a more direct competitor.

### Mitigations
- **Move fast** — establish MindFizz as the authoritative UK voice on MCP security before SPLX or others claim the space
- **Build relationships** with Anthropic's MCP team — position as complementary ecosystem tool, not competition
- **Contribute upstream** to OWASP/CSA — being part of the standards body prevents being disrupted by it
- **Differentiate on services** — tools can be replicated, trusted advisory relationships cannot

---

## 10. Summary

The MCP security market is **extremely early-stage** — there are essentially no established companies focused specifically on this niche. This represents a rare greenfield opportunity. The key competitors are:

1. **Direct tool competitors:** cc-fuyu (open source npm), mcpscan.ai (cloud SaaS) — neither offers consulting
2. **Broad AI security platforms:** Adversa, Enkrypt, SPLX — enterprise pricing, broader focus
3. **Traditional UK cyber firms:** OnSecurity, GoDefend, CybaVerse — no AI agent expertise

**MindFizz's winning position:** The UK's MCP security specialist — open source tooling (local-first, privacy-preserving) backed by expert consulting services. Target the underserved mid-market between free tools and £100K+ enterprise platforms.

**Urgency:** SPLX is the primary threat. They're UK-based, funded, and already mention MCP in their platform. MindFizz needs to establish brand authority in MCP security within the next 3-6 months.
