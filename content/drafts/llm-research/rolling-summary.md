# LLM Landscape — Rolling Summary

> Last updated: 2026-03-16

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
| NVIDIA Nemotron 3 Super | 120B (12B) | Mamba-2+MoE+Attn | 1M | NVIDIA Open | Agentic, long-context king |
| Sarvam-105B | 105B (10.3B) | MoE+MLA | 128K | Apache 2.0 | Indian languages, strong reasoning |
| MiniMax M2.5 | 229B (MoE) | Transformer | — | Open weights | Released alongside API |
| Qwen3.5-122B-A10B | 122B (~10B) | MoE | — | — | Reference in Nemotron benchmarks |

## Mid-Size Open Models (7B-35B) — Worth Running Locally

| Model | Size | Architecture | Best For | Fits On |
|-------|------|-------------|----------|---------|
| **Qwen3.5-9B** | 9B | Hybrid (Gated Delta + Attn) | General, multimodal | 1× 3090 |
| **Qwen3.5-27B** | 27B | — | General, reasoning | 2× 3090 |
| **Qwen3.5-35B-A3B** | 35B (3B active) | MoE | Efficient general | 1× 3090 |
| **OmniCoder-9B** | 9B | Qwen3.5-9B base | Coding agents | 1× 3090 |
| **Reka Edge** | 7B | Multimodal VLM | Vision, edge deploy | Mac mini / 1× 3090 |
| Qwen3.5-4B | 4B | — | Ultra-light general | Any GPU / CPU |

## TTS / Speech Models

| Model | Size | Type | Notable |
|-------|------|------|---------|
| Fish Audio S2 Pro | 5B | TTS | 80+ languages, inline emotion tags, RL-aligned |
| **HumeAI TADA** | 1B/3B | TTS | 1:1 text-acoustic alignment, zero hallucination, 5× faster, MIT license |
| **IBM Granite 4.0-1b-speech** | 1B | ASR/AST | #1 OpenASR leaderboard, 6 languages + Japanese, keyword biasing, Apache 2.0 |

## Key Trends (as of mid-March 2026)

1. **MoE dominance**: Every new frontier model is MoE. Active params matter more than total. 10-12B active in 100B+ shells is the sweet spot.
2. **Distillation gold rush**: Community fine-tunes distilling Claude Opus 4.6 reasoning into Qwen3.5 bases. OmniCoder shows this works remarkably well.
3. **Hybrid architectures**: Mamba-2, Gated Delta Networks, and attention hybrids are standard. Pure transformers feel old.
4. **Agentic benchmarks matter**: SWE-Bench, Terminal-Bench, τ² Bench, BrowseComp now defining model quality more than MMLU.
5. **Cost collapse**: MiniMax M2.5 at 10-20× cheaper than Opus for similar coding performance. Agentic workloads becoming economically viable.
6. **Edge multimodal**: Reka Edge shows 7B VLMs can rival much larger models with smarter tokenization (331 vs 1000+ tokens per image).
7. **Long-context pricing wars**: Anthropic eliminates long-context premium entirely (flat rate to 1M). OpenAI/Google still charge more above 200-272K tokens.
8. **Local AI infrastructure consolidating**: GGML/llama.cpp joining HF signals maturation of local inference ecosystem.
9. **Agentic RAG maturing**: NVIDIA NeMo Retriever shows ReACT-based iterative retrieval beating single-shot approaches significantly.
10. **Autoresearch pattern emerging**: Automated benchmark-driven optimization (Shopify/Karpathy) proving effective for systematic code improvement.

## Recent Moves (March 14–16)

- **Anthropic**: 1M context GA for Opus/Sonnet 4.6 at standard pricing — major competitive advantage
- **Meta**: Reportedly planning ~20% layoffs (~16K people) to offset AI infrastructure costs ($600B committed through 2028)
- **NVIDIA**: NeMo Retriever agentic pipeline tops ViDoRe v3 and BRIGHT benchmarks
- **Hume AI**: Open-sourced TADA (TTS), MIT license, 1B/3B params, zero hallucination
- **IBM**: Granite 4.0 1B Speech — #1 on OpenASR, Apache 2.0
- **Ai2**: MolmoBot — robot manipulation trained entirely in simulation, zero-shot real-world transfer
- **Bytedance**: Seedance 2.0 global launch shelved due to Hollywood copyright pushback

## Models to Watch

- **MiniMax M2.5** — Could be game-changing for cost-sensitive agentic work. Need real-world testing.
- **Qwen3.5 ecosystem** — The new "base model" for community. Expect rapid iteration.
- **Nemotron 3 Super** — NVIDIA open models getting serious. FP4 quantization opens hardware doors.
- **Reka Edge** — Best vision per parameter. Edge deployment story is compelling.
- **Claude Opus 4.6** — Still the benchmark. Now with 1M context at flat rate — hard to beat for complex work.
- **TADA (Hume AI)** — Potential game-changer for local TTS. MIT license, runs on consumer GPUs.

## Our Hardware Fit (Mac mini + 5× RTX 3090 24GB)

**Can run now:**
- Qwen3.5-9B, 27B (quantized), 35B-A3B, 4B
- OmniCoder-9B
- Reka Edge 7B
- TADA 1B/3B (NEW — MIT, great for local TTS)
- IBM Granite 4.0 1B Speech (NEW — Apache 2.0, local ASR)
- Any community distill ≤9B

**Could run with effort:**
- Sarvam-105B (10.3B active, but need full model in memory — possible with aggressive quantization across 5×3090)
- Nemotron 3 Super FP4 (67GB FP4 — could fit across 5×3090 120GB total, tight)

**API only:**
- Claude Opus 4.6, Sonnet 4.6 (now with 1M context at flat rate)
- GPT-5/5.4
- Gemini 3.1 Pro
- MiniMax M2.5 (consider for cost savings)

---

*This summary is updated with each nightly research run.*
