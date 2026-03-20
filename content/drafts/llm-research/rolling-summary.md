# LLM Landscape — Rolling Summary

> Last updated: 2026-03-20

---

## Frontier Models (Closed-Source API)

| Provider | Model | Released | Key Strengths | Pricing (per M tokens) |
|----------|-------|----------|---------------|----------------------|
| Anthropic | Claude Opus 4.6 | ~Jan 2026 | Best overall reasoning, coding, agentic, **1M context GA at flat rate** | $5 in / $25 out |
| Anthropic | Claude Sonnet 4.6 | Feb 17, 2026 | Frontier at lower cost, coding/agents, **1M context GA** | $3 in / $15 out |
| Anthropic | Claude Haiku 4.5 | ~2025 | Fast, cheap, good enough | ~$1 in / $5 out |
| OpenAI | GPT-5.4 | Mar 5, 2026 | Latest frontier, 1M context (surcharge >272K) | $2.50 in / $15 out |
| OpenAI | **GPT-5.4 mini** | **Mar 17, 2026** | **Fast coding/computer-use, 400K context, subagent-optimized** | **$0.75 in / $4.50 out** |
| OpenAI | **GPT-5.4 nano** | **Mar 17, 2026** | **Cheapest frontier model, classification/extraction** | **$0.20 in / $1.25 out** |
| Google | Gemini 3.1 Pro | Feb 19, 2026 | Strong multimodal, long context, surcharge >200K tokens | ~$2 in / $12 out |
| Google | Gemini 3.1 Flash-Lite | Mar 3, 2026 | High-volume speed tasks | $0.25 in / $1.50 out |
| MiniMax | M2.5 | Feb 2026 | SOTA SWE-Bench 80.2%, cheapest frontier | $0.15-0.30 in / $1.20-2.40 out |

## Open-Weight Frontier (100B+)

| Model | Params (active) | Architecture | Context | License | Notes |
|-------|-----------------|-------------|---------|---------|-------|
| **Mistral Small 4** | 119B (6.5B) | MoE 128×4 | 256K | Apache 2.0 | Unified instruct/reasoning/code, multimodal, NVFP4 available |
| **Leanstral** | 119B (6.5B) | MoE (MS4 base) | 256K | Apache 2.0 | First open-source Lean 4 theorem proving agent |
| NVIDIA Nemotron 3 Super | 120B (12B) | Mamba-2+MoE+Attn | 1M | NVIDIA Open | Agentic, long-context king |
| Sarvam-105B | 105B (10.3B) | MoE+MLA | 128K | Apache 2.0 | Indian languages, strong reasoning |
| MiniMax M2.5 | 229B (MoE) | Transformer | — | Open weights | SOTA SWE-Bench at fraction of cost |
| MiroThinker 1.7 | 235B | — | 256K | — | Deep research agent, 300 tool calls, SOTA BrowseComp-ZH |
| Qwen3.5-122B-A10B | 122B (~10B) | MoE | — | Apache 2.0 | Strong general-purpose |
| GLM-5 | 355B | — | — | — | HumanEval 94.2, SWE-bench 73.8 |

## Mystery / Unconfirmed

| Model | Params | Context | Status | Notes |
|-------|--------|---------|--------|-------|
| **Hunter Alpha** | **~1T** | **1M** | **Anonymous on OpenRouter since Mar 11** | **Suspected DeepSeek V4 test. 160B+ tokens processed. Free. Chinese origin, May 2025 cutoff.** |

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
| **HumeAI TADA** | 1B/3B/3B-ml | TTS | 1:1 text-acoustic alignment, zero hallucination, 5× faster, MIT license. 3B-ml adds multilingual |
| **IBM Granite 4.0-1b-speech** | 1B | ASR/AST | #1 OpenASR leaderboard, 6 languages + Japanese, keyword biasing, Apache 2.0 |

## Key Trends (as of March 19, 2026)

1. **MoE dominance**: Every new frontier model is MoE. Active params matter more than total. 6-12B active in 100B+ shells is the sweet spot.
2. **Unified models**: Mistral Small 4 combines instruct/reasoning/coding in one model with per-request reasoning effort control. Expect others to follow.
3. **Hub-spoke agent architectures**: OpenAI explicitly pushing GPT-5.4 + mini/nano subagent pattern. Large model plans, small models execute in parallel. This is the template for 2026 agentic systems.
4. **Cost collapse accelerating**: GPT-5.4 nano at $0.20/$1.25 undercuts Gemini Flash-Lite. MiniMax M2.5 at $0.15 input. Agentic workloads now economically viable at scale.
5. **Hybrid architectures**: Mamba-2, Gated Delta Networks, and attention hybrids are standard. Pure transformers feel old.
6. **Agentic benchmarks matter**: SWE-Bench, BrowseComp, GAIA, OSWorld, Toolathlon now defining model quality more than MMLU.
7. **Deep research agents emerging**: MiroThinker 1.7 (300 tool calls), Cowork persistent threads — "agent models" purpose-built for long-chain tasks.
8. **Distillation gold rush**: Community fine-tunes distilling Claude Opus 4.6 reasoning into Qwen3.5 bases.
9. **Long-context pricing wars**: Anthropic flat rate to 1M. OpenAI/Google still surcharge above 200-272K.
10. **Hardware race**: NVIDIA Vera Rubin (10× perf/watt), Groq 3 LPU (35× tokens/watt), Feynman/Kyber previewed. $1T projected revenue.
11. **Anonymous model testing**: Hunter Alpha on OpenRouter shows labs may be doing stealth testing in production. DeepSeek V4 rumored April.

## Recent Moves (March 17–20)

- **OpenAI**: Released **GPT-5.4 mini** ($0.75/$4.50, 400K context) and **GPT-5.4 nano** ($0.20/$1.25, cheapest frontier). **GPT-5.3 Instant** rolling out as new default ChatGPT model (↓27% hallucination on web search). ChatGPT model picker redesigned into Instant/Thinking/Pro tiers.
- **NVIDIA GTC 2026** (March 16-19): Vera Rubin platform, Groq 3 LPU, Feynman architecture, Kyber rack prototype, DLSS 5, NemoClaw for OpenClaw. $1T revenue projection. **SPEED-Bench** published (Mar 19) — unified speculative decoding benchmark.
- **Google**: Gemini API Built-in Tools + Function Calling (March 18). **Stitch design platform live** — AI vibe design tool. **Vibe coding in AI Studio** with Gemini 3.1 Pro.
- **Anthropic** (March 17): Persistent Cowork agent thread for Pro/Max. 2× usage promo continues through March 28.
- **H Company × NVIDIA**: **Holotron-12B** released (Mar 17) — open-weight 12B computer-use agent with hybrid SSM, 2× throughput on single H100.
- **Hunter Alpha mystery** (March 11→): 1T-param anonymous model on OpenRouter, suspected DeepSeek V4. 160B+ tokens processed. Active speculation.
- **Meta Avocado**: Still delayed to May+. Performance concerns. **Meta AI agent caused Sev-1 security breach** — autonomous forum post → 2hr unauthorized data access.
- **Mistral**: Released Mistral Small 4 (March 15), Leanstral, **Forge** (Mar 17) — enterprise custom model training on proprietary data.
- **MiroMind AI**: MiroThinker 1.7 (30B/235B) deep research agents.
- **Hugging Face**: State of Open Source Spring 2026 report — 13M users, 2M+ models. GGML/llama.cpp joined HF. Storage Buckets launched.

## Models to Watch

- **Hunter Alpha / DeepSeek V4** — If confirmed open-weight, 1T model with 1M context is transformative. April timeline rumored.
- **GPT-5.4 nano** — Cheapest frontier model. Test for lightweight OpenClaw subagent tasks immediately.
- **Holotron-12B** — NEW. Open-weight 12B computer-use agent with SSM. Could run on 1-2× 3090. Test for local CUA.
- **Mistral Small 4 NVFP4** — 6.5B active, Apache 2.0, might fit across 5×3090. Top priority for local testing.
- **Mistral Forge** — Enterprise custom model training. Watch for pricing/availability details.
- **MiniMax M2.5** — Game-changing for cost-sensitive agentic work.
- **NemoClaw** — NVIDIA security wrapper for OpenClaw. Directly relevant.
- **Qwen3.5 ecosystem** — The "base model" for community. Rapid iteration continues.
- **Claude Opus 4.6** — Still the benchmark. 1M context at flat rate — hard to beat for complex work.
- **Meta Avocado** — Delayed to May+. If open-weight, could be significant.
- **Gemini 3.1 + Tools combo** — New API feature worth testing for search-grounded workflows.

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
- **Holotron-12B** — 12B SSM hybrid, efficient computer-use agent. Should fit on 1-2× 3090.

**Could run with effort:**
- Sarvam-105B (10.3B active, aggressive quantization across 5×3090)
- Nemotron 3 Super FP4 (67GB FP4 — tight fit across 5×3090)

**API only:**
- Claude Opus 4.6, Sonnet 4.6 (1M context at flat rate)
- GPT-5.4 / 5.4-mini / 5.4-nano
- Gemini 3.1 Pro / Flash-Lite
- MiniMax M2.5

**Cost optimization note:** For high-volume agentic subtasks, GPT-5.4 nano ($0.20/$1.25) is now cheaper than running local models when factoring electricity + GPU wear. Consider hybrid: local for privacy-sensitive, nano for everything else.

---

*This summary is updated with each nightly research run.*
