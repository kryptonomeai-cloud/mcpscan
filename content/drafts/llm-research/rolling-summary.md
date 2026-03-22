# LLM Landscape — Rolling Summary

> Last updated: 2026-03-22

---

## Frontier Models (Closed-Source API)

| Provider | Model | Released | Key Strengths | Pricing (per M tokens) |
|----------|-------|----------|---------------|----------------------|
| Anthropic | Claude Opus 4.6 | ~Jan 2026 | Best overall reasoning, coding, agentic, **1M context GA at flat rate** | $5 in / $25 out |
| Anthropic | Claude Sonnet 4.6 | Feb 17, 2026 | Frontier at lower cost, coding/agents, **1M context GA** | $3 in / $15 out |
| Anthropic | Claude Haiku 4.5 | ~2025 | Fast, cheap, good enough | ~$1 in / $5 out |
| OpenAI | GPT-5.4 | Mar 5, 2026 | Latest frontier, 1M context (surcharge >272K) | $2.50 in / $15 out |
| OpenAI | GPT-5.4 mini | Mar 17, 2026 | Fast coding/computer-use, 400K context, subagent-optimized | $0.75 in / $4.50 out |
| OpenAI | GPT-5.4 nano | Mar 17, 2026 | Cheapest frontier model, classification/extraction | $0.20 in / $1.25 out |
| Google | Gemini 3.1 Pro | Feb 19, 2026 | Strong multimodal, long context, surcharge >200K tokens | ~$2 in / $12 out |
| Google | Gemini 3.1 Flash-Lite | Mar 3, 2026 | High-volume speed tasks | $0.25 in / $1.50 out |
| MiniMax | M2.5 | Feb 2026 | SOTA SWE-Bench 80.2%, cheapest frontier | $0.15-0.30 in / $1.20-2.40 out |
| **MiniMax** | **M2.7** | **Mar 20, 2026** | **Self-evolving RL, SWE-Pro 56.22%, low hallucination (34%)** | **TBD (proprietary)** |
| **Xiaomi** | **MiMo-V2-Pro** | **Mar 20, 2026** | **1T sparse (42B active), 1M context, #10 AA Index** | **~1/6th Opus/GPT-5.2 pricing** |

## Open-Weight Frontier (100B+)

| Model | Params (active) | Architecture | Context | License | Notes |
|-------|-----------------|-------------|---------|---------|-------|
| Mistral Small 4 | 119B (6.5B) | MoE 128×4 | 256K | Apache 2.0 | Unified instruct/reasoning/code, multimodal, NVFP4 available |
| Leanstral | 119B (6.5B) | MoE (MS4 base) | 256K | Apache 2.0 | First open-source Lean 4 theorem proving agent |
| NVIDIA Nemotron 3 Super | 120B (12B) | Mamba-2+MoE+Attn | 1M | NVIDIA Open | Agentic, long-context king |
| **NVIDIA Nemotron Cascade 2** | **30B (3B)** | **Distilled** | **TBD** | **TBD** | **NEW — just uploaded to HF, efficient agent model** |
| Sarvam-105B | 105B (10.3B) | MoE+MLA | 128K | Apache 2.0 | Indian languages, strong reasoning |
| MiniMax M2.5 | 229B (MoE) | Transformer | — | Open weights | SOTA SWE-Bench at fraction of cost |
| MiroThinker 1.7 | 235B | — | 256K | — | Deep research agent, 300 tool calls, SOTA BrowseComp-ZH |
| Qwen3.5-122B-A10B | 122B (~10B) | MoE | — | Apache 2.0 | Strong general-purpose |
| GLM-5 | 355B | — | — | — | HumanEval 94.2, SWE-bench 73.8 |

## Mystery / Unconfirmed

| Model | Params | Context | Status | Notes |
|-------|--------|---------|--------|-------|
| Hunter Alpha | ~1T | 1M | Anonymous on OpenRouter since Mar 11 | Suspected DeepSeek V4 test. 160B+ tokens processed. Free. Chinese origin, May 2025 cutoff. |

## Mid-Size Open Models (7B-35B) — Worth Running Locally

| Model | Size | Architecture | Best For | Fits On |
|-------|------|-------------|----------|---------|
| **Nemotron Cascade 2 30B-A3B** | **30B (3B active)** | **Distilled** | **Efficient agent** | **1× 3090** |
| Qwen3.5-9B | 9B | Hybrid (Gated Delta + Attn) | General, multimodal | 1× 3090 |
| Qwen3.5-27B | 27B | — | General, reasoning | 2× 3090 |
| Qwen3.5-35B-A3B | 35B (3B active) | MoE | Efficient general | 1× 3090 |
| **Qwen3.5-27B-Claude-4.6-Opus-Distilled** | **27B** | **Qwen3.5 + Opus distill** | **Reasoning** | **2× 3090 (Q4)** |
| MiroThinker 1.7-mini | 30B | — | Deep research agent | 2× 3090 |
| OmniCoder-9B | 9B | Qwen3.5-9B base | Coding agents | 1× 3090 |
| Reka Edge | 7B | Multimodal VLM | Vision, edge deploy | Mac mini / 1× 3090 |
| Qwen3.5-4B | 4B | — | Ultra-light general | Any GPU / CPU |

## TTS / Speech Models

| Model | Size | Type | Notable |
|-------|------|------|---------|
| Fish Audio S2 Pro | 5B | TTS | 80+ languages, inline emotion tags, RL-aligned |
| HumeAI TADA | 1B/3B/3B-ml | TTS | 1:1 text-acoustic alignment, zero hallucination, 5× faster, MIT license |
| IBM Granite 4.0-1b-speech | 1B | ASR/AST | #1 OpenASR leaderboard, 6 languages + Japanese, Apache 2.0 |

## Key Trends (as of March 21, 2026)

1. **MoE dominance**: Every new frontier model is MoE. Active params matter more than total. 6-12B active in 100B+ shells is the sweet spot.
2. **Self-evolving models**: MiniMax M2.7 did 30-50% of its own RL training. Recursive self-improvement is no longer theoretical.
3. **Chinese proprietary pivot**: MiniMax (M2.7), z.ai (GLM-5 Turbo), and rumored Alibaba/Qwen shifting from open-source to proprietary. The free lunch may be ending.
4. **Hub-spoke agent architectures**: OpenAI explicitly pushing GPT-5.4 + mini/nano subagent pattern. Cursor building model in-house (Composer 2). Vertical integration accelerating.
5. **Cost collapse accelerating**: GPT-5.4 nano at $0.20/$1.25, MiMo-V2-Pro at ~1/6th frontier pricing, Composer 2 at 86% cheaper than predecessor.
6. **Hybrid architectures**: Mamba-3 released (Apache 2.0) with inference-first design. Mamba-2, Gated Delta Networks, and attention hybrids are now standard.
7. **Inference optimization**: Nvidia KVTC shrinks KV cache 20× without weight changes. This is the bottleneck everyone's attacking.
8. **Agentic benchmarks matter**: SWE-Bench, Terminal-Bench 2.0, GDPval-AA, MLE Bench Lite now defining model quality more than MMLU.
9. **Deep research agents emerging**: MiroThinker 1.7 (300 tool calls), Cowork persistent threads — "agent models" purpose-built for long-chain tasks.
10. **Distillation gold rush**: Community distilling Opus 4.6 reasoning into Qwen3.5 bases. Trending heavily on HuggingFace. v2 distills appearing.
11. **Privacy in AI chat**: Moxie Marlinspike (Signal creator) integrating Confer encrypted AI into Meta AI. Could make encrypted LLM inference mainstream.
12. **NemoClaw / OpenClaw ecosystem**: Nvidia officially wrapping OpenClaw for enterprise. Jensen called it "the operating system for personal AI."
13. **Tool acquisitions for coding**: OpenAI buying Astral (Ruff/uv/ty) signals that owning dev tools is the new moat. Expect more M&A.
14. **Always-on agents**: Claude Code channels + OpenClaw + NemoClaw — the industry is converging on persistent, event-driven AI assistants.
15. **Custom model training from base**: Cursor's Composer 2 (Kimi K2.5 + continued pretraining + RL) is the playbook: take open/licensed base, specialize via training, not just prompting.

## Recent Moves (March 19–22)

- **OpenAI**: Acquiring **Astral** (Ruff/uv/ty) for Codex team. Tools staying open source. Desktop "superapp" confirmed (ChatGPT+Codex+Atlas). Hiring from 4,500→8,000.
- **Anthropic**: Claude Code **channels** (research preview) — Telegram/Discord two-way messaging into running sessions. Moving toward always-on agent territory.
- **Cursor**: Launched **Composer 2** (fine-tuned Kimi K2.5 via Fireworks AI, $0.50/$2.50). CursorBench 61.3, Terminal-Bench 61.7, SWE-bench ML 73.7.
- **Nvidia**: **Nemotron Cascade 2 30B-A3B** uploaded to HF (Mar 22). **Nemotron 3 Super 120B** BF16/NVFP4 updated. **NemoClaw** enterprise wrapper launched at GTC.
- **Xiaomi**: Released **MiMo-V2-Pro** (1T sparse, 42B active, 1M context). #10 on Artificial Analysis. Open-source variant planned.
- **MiniMax**: Released **M2.7** (proprietary, self-evolving RL, SWE-Pro 56.22%). Chinese labs going proprietary.
- **Mistral**: **Forge** enterprise custom model training announced (Mar 17). **Leanstral** (Lean 4 theorem proving agent).
- **Microsoft**: **MAI-Image-2** launched. Rolling out in Copilot/Bing.
- **Meta**: AI replacing content moderators. Confer encryption partnership with Moxie Marlinspike.
- **WordPress.com**: MCP write capabilities — AI agents can now create/publish content.
- **Pentagon vs Anthropic**: DoD filed rebuttal calling Anthropic a "supply chain risk" in ongoing lawsuit.
- **Flash-MoE**: Qwen 397B running at 5.5 t/s on 48GB M3 Max via "LLM in a Flash" techniques.

## Models to Watch

- **Hunter Alpha / DeepSeek V4** — If confirmed open-weight, 1T model with 1M context is transformative. April timeline rumored.
- **MiMo-V2-Pro open variant** — Xiaomi planning open-source release. At 42B active, could reshape local deployment.
- **Nemotron Cascade 2 30B-A3B** — NEW. 3B active, could be excellent local agent. Test immediately.
- **Qwen3.5-27B-Opus-Distilled** — Community distill with 958 likes. Priority test for local reasoning.
- **GPT-5.4 nano** — Cheapest frontier model at $0.20/$1.25. Test for lightweight subagent tasks.
- **Holotron-12B** — Open-weight 12B computer-use agent with SSM. Could run on 1-2× 3090.
- **Mistral Small 4 NVFP4** — 6.5B active, Apache 2.0, might fit across 5×3090.
- **Claude Code channels** — Anthropic building OpenClaw-like functionality into Claude Code. Watch for GA and API key support.
- **OpenAI superapp** — When it ships, this consolidates ChatGPT+Codex+Atlas. May change how we interact with OpenAI APIs.
- **Mistral Forge** — Enterprise custom model training. Watch for pricing/availability.
- **MiniMax M2.7 API** — Self-evolving model. Test when pricing is published.
- **Mamba 3 derivatives** — Watch for community scaling this architecture to larger models.
- **Claude Opus 4.6** — Still the benchmark. 1M context at flat rate.
- **Meta Avocado** — Delayed to May+. If open-weight, could be significant.
- **NemoClaw** — Nvidia enterprise wrapper for OpenClaw. Directly relevant.

## Our Hardware Fit (Mac mini + 5× RTX 3090 24GB)

**Can run now:**
- Qwen3.5-9B, 27B (quantized), 35B-A3B, 4B
- OmniCoder-9B
- Reka Edge 7B
- TADA 1B/3B/3B-ml (MIT, great for local TTS)
- IBM Granite 4.0 1B Speech (Apache 2.0, local ASR)
- MiroThinker 1.7-mini (30B, quantized on 2× 3090)
- Any community distill ≤9B

**Priority tests this week:**
- **Nemotron Cascade 2 30B-A3B** — 3B active, should fit easily on 1× 3090. Brand new.
- **Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled** — GGUF available, 2× 3090 at Q4.
- **Mistral Small 4 NVFP4** — 67GB, tight fit across 5× 3090 (120GB total).

**Could run with effort:**
- Sarvam-105B (10.3B active, aggressive quantization across 5×3090)
- Nemotron 3 Super FP4 (67GB FP4 — tight fit across 5×3090)

**API only:**
- Claude Opus 4.6, Sonnet 4.6 (1M context at flat rate)
- GPT-5.4 / 5.4-mini / 5.4-nano
- Gemini 3.1 Pro / Flash-Lite
- MiniMax M2.5 / M2.7
- MiMo-V2-Pro (until open variant releases)

**Cost optimization note:** For high-volume agentic subtasks, GPT-5.4 nano ($0.20/$1.25) is now cheaper than running local models when factoring electricity + GPU wear. MiMo-V2-Pro may offer an even better ratio. Consider hybrid: local for privacy-sensitive, cheapest API for everything else.

---

*This summary is updated with each nightly research run.*
