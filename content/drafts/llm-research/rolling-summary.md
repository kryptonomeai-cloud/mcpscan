# LLM Landscape — Rolling Summary

> Last updated: 2026-03-18

---

## Frontier Models (Closed-Source API)

| Provider | Model | Released | Key Strengths | Pricing (per M tokens) |
|----------|-------|----------|---------------|----------------------|
| Anthropic | Claude Opus 4.6 | ~Jan 2026 | Best overall reasoning, coding, agentic, **1M context GA at flat rate** | $5 in / $25 out |
| Anthropic | Claude Sonnet 4.6 | Feb 17, 2026 | Frontier at lower cost, coding/agents, **1M context GA** | $3 in / $15 out |
| Anthropic | Claude Haiku 4.5 | ~2025 | Fast, cheap, good enough | ~$0.25 in / $1.25 out |
| OpenAI | GPT-5 | ~2025-2026 | Strong general, multimodal | Varies by tier |
| OpenAI | GPT-5.4 | ~2026 | Latest iteration, surcharge >272K tokens | Varies |
| Google | Gemini 3.1 Pro | ~2026 | Strong multimodal, long context, surcharge >200K tokens | Varies |
| MiniMax | M2.5 | Mar 2026 | SOTA SWE-Bench 80.2%, cheapest frontier | $0.15-0.30 in / $1.20-2.40 out |

## Open-Weight Frontier (100B+)

| Model | Params (active) | Architecture | Context | License | Notes |
|-------|-----------------|-------------|---------|---------|-------|
| **Mistral Small 4** | 119B (6.5B) | MoE 128×4 | 256K | Apache 2.0 | Unified instruct/reasoning/code, multimodal, NVFP4 available |
| **Leanstral** | 119B (6.5B) | MoE (MS4 base) | 256K | Apache 2.0 | **NEW** — First open-source Lean 4 theorem proving agent |
| NVIDIA Nemotron 3 Super | 120B (12B) | Mamba-2+MoE+Attn | 1M | NVIDIA Open | Agentic, long-context king |
| Sarvam-105B | 105B (10.3B) | MoE+MLA | 128K | Apache 2.0 | Indian languages, strong reasoning |
| MiniMax M2.5 | 229B (MoE) | Transformer | — | Open weights | SOTA SWE-Bench at fraction of cost |
| MiroThinker 1.7 | 235B | — | 256K | — | **NEW** — Deep research agent, 300 tool calls, SOTA BrowseComp-ZH |
| Qwen3.5-122B-A10B | 122B (~10B) | MoE | — | — | Reference in Nemotron benchmarks |

## Mid-Size Open Models (7B-35B) — Worth Running Locally

| Model | Size | Architecture | Best For | Fits On |
|-------|------|-------------|----------|---------|
| **Qwen3.5-9B** | 9B | Hybrid (Gated Delta + Attn) | General, multimodal | 1× 3090 |
| **Qwen3.5-27B** | 27B | — | General, reasoning | 2× 3090 |
| **Qwen3.5-35B-A3B** | 35B (3B active) | MoE | Efficient general | 1× 3090 |
| **MiroThinker 1.7-mini** | 30B | — | Deep research agent | 2× 3090 |
| **OmniCoder-9B** | 9B | Qwen3.5-9B base | Coding agents | 1× 3090 |
| **Reka Edge** | 7B | Multimodal VLM | Vision, edge deploy | Mac mini / 1× 3090 |
| Qwen3.5-4B | 4B | — | Ultra-light general | Any GPU / CPU |

## TTS / Speech Models

| Model | Size | Type | Notable |
|-------|------|------|---------|
| Fish Audio S2 Pro | 5B | TTS | 80+ languages, inline emotion tags, RL-aligned |
| **HumeAI TADA** | 1B/3B/3B-ml | TTS | 1:1 text-acoustic alignment, zero hallucination, 5× faster, MIT license. **3B-ml adds multilingual** |
| **IBM Granite 4.0-1b-speech** | 1B | ASR/AST | #1 OpenASR leaderboard, 6 languages + Japanese, keyword biasing, Apache 2.0 |

## Key Trends (as of mid-March 2026)

1. **MoE dominance**: Every new frontier model is MoE. Active params matter more than total. 6-12B active in 100B+ shells is the sweet spot.
2. **Unified models**: Mistral Small 4 combines instruct/reasoning/coding in one model with per-request reasoning effort control. Expect others to follow.
3. **Distillation gold rush**: Community fine-tunes distilling Claude Opus 4.6 reasoning into Qwen3.5 bases. OmniCoder shows this works remarkably well.
4. **Hybrid architectures**: Mamba-2, Gated Delta Networks, and attention hybrids are standard. Pure transformers feel old.
5. **Agentic benchmarks matter**: SWE-Bench, BrowseComp, GAIA now defining model quality more than MMLU.
6. **Deep research agents emerging**: MiroThinker 1.7 (300 tool calls) shows the pattern of "agent models" purpose-built for long-chain research.
7. **Cost collapse**: MiniMax M2.5 at 10-20× cheaper than Opus for similar coding performance. Agentic workloads becoming economically viable.
8. **Edge multimodal**: Reka Edge shows 7B VLMs can rival much larger models with smarter tokenization (331 vs 1000+ tokens per image).
9. **Long-context pricing wars**: Anthropic eliminates long-context premium entirely (flat rate to 1M). OpenAI/Google still charge more above 200-272K tokens.
10. **Speculation + quantization**: Mistral's eagle head for speculative decoding + NVFP4 checkpoints show inference optimization is as important as training.

## Recent Moves (March 15–18)

- **Mistral**: Released Mistral Small 4 (119B, 6.5B active) — unified instruct/reasoning/code, Apache 2.0, NVFP4 available. Also released **Leanstral** (Lean 4 theorem prover) and **Forge** (enterprise fine-tuning platform).
- **NVIDIA GTC 2026**: Announced **NemoClaw** — security/privacy wrapper for OpenClaw. Jensen calls OpenClaw "the OS for personal AI." Also teased Vera Ruben Space 1 (AI data centers in space).
- **Google**: Expanding Gemini Personal Intelligence to free-tier users in Gemini app and Chrome.
- **OpenAI**: Refocusing on coding + enterprise, deprioritizing Sora, Atlas browser, and hardware gadgets.
- **Meta Avocado**: Delayed from March to May+. Performance reportedly lags rivals.
- **Moltbook** (Meta-acquired): Updated ToS — users "solely responsible" for AI agent actions.
- **MiroMind AI**: MiroThinker 1.7 (30B/235B) — deep research agents, SOTA BrowseComp-ZH
- **Hume AI**: TADA 3B-ml multilingual update
- **IBM**: Granite 4.0-1b-speech iterating (Japanese ASR, keyword biasing)

## Models to Watch

- **Mistral Small 4 NVFP4** — NEW. 6.5B active, Apache 2.0, might fit our hardware. Top priority for testing.
- **MiniMax M2.5** — Game-changing for cost-sensitive agentic work. Need real-world testing.
- **Qwen3.5 ecosystem** — The "base model" for community. Rapid iteration continues.
- **MiroThinker 1.7-mini (30B)** — If deep research tasks needed locally.
- **Nemotron 3 Super** — NVIDIA open models getting serious. FP4 quantization opens hardware doors.
- **Reka Edge** — Best vision per parameter. Edge deployment story is compelling.
- **Claude Opus 4.6** — Still the benchmark. 1M context at flat rate — hard to beat for complex work.
- **TADA (Hume AI)** — Local TTS game-changer. MIT license, now multilingual.
- **Alibaba enterprise agent** — Watch for this week's announcement. Qwen-based, Taobao/Alipay integrated.
- **NemoClaw** — NVIDIA's security wrapper for OpenClaw. Directly relevant to our setup.
- **Meta Avocado** — Delayed to May+. If open-weight, could be significant.

## Our Hardware Fit (Mac mini + 5× RTX 3090 24GB)

**Can run now:**
- Qwen3.5-9B, 27B (quantized), 35B-A3B, 4B
- OmniCoder-9B
- Reka Edge 7B
- TADA 1B/3B/3B-ml (MIT, great for local TTS)
- IBM Granite 4.0 1B Speech (Apache 2.0, local ASR)
- MiroThinker 1.7-mini (30B, quantized on 2× 3090)
- Any community distill ≤9B

**Should test:**
- **Mistral Small 4 NVFP4** — 6.5B active, needs full model loaded. NVFP4 checkpoint may fit across 5×3090 (120GB total). HIGH PRIORITY.

**Could run with effort:**
- Sarvam-105B (10.3B active, aggressive quantization across 5×3090)
- Nemotron 3 Super FP4 (67GB FP4 — tight fit across 5×3090)

**API only:**
- Claude Opus 4.6, Sonnet 4.6 (1M context at flat rate)
- GPT-5/5.4
- Gemini 3.1 Pro
- MiniMax M2.5 (consider for cost savings on agentic work)

---

*This summary is updated with each nightly research run.*
