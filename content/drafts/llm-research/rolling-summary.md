# LLM Landscape — Rolling Summary

_Last updated: 2026-03-23_

---

## Current Frontier Models (as of Mar 2026)

### Closed-Source
| Provider | Model | Released | Key Strength |
|----------|-------|----------|-------------|
| Anthropic | Claude Opus 4.6 | Feb 2026 | Best overall quality, agentic coding, tool use |
| OpenAI | GPT-OSS-120B | ~2026 | Referenced as benchmark baseline across papers |
| Google | Gemini (current gen) | Ongoing | Multimodal, search integration |
| MiniMax | M2.5 (229B) | Mar 2026 | SOTA SWE-Bench (80.2%), cheapest frontier API |

### Open-Source / Open-Weight
| Provider | Model | Params (Active) | Context | License | Key Strength |
|----------|-------|-----------------|---------|---------|-------------|
| Qwen | 3.5 family | 4B–397B-A17B | 262k–1M | Apache 2.0 | Best all-round open family, multimodal, 201 langs |
| Mistral | Small 4 | 119B (6.5B) | 256k | Apache 2.0 | Unified instruct/reasoning/multimodal, efficient |
| NVIDIA | Nemotron Cascade 2 | 30B (3B) | — | Nemotron Open | Olympiad-gold math/code in tiny footprint |
| NVIDIA | Nemotron 3 Super | 120B (12B) | 1M | Nemotron Open | Mamba-2 hybrid, MTP, best 1M context |
| Mistral | Leanstral | 119B (6B) | 256k | Apache 2.0 | Lean 4 proof engineering |
| Rakuten | AI 3.0 | 671B (37B) | 128k | Apache 2.0 | Japanese-optimized |

---

## Key Trends

### 1. MoE Efficiency Revolution
The 3-6B active parameter MoE models are the story of Q1 2026. Models like Nemotron Cascade 2 (3B active) achieving IMO gold, and Qwen3.5-35B-A3B being the most downloaded model on HuggingFace, prove that sparse expert routing is the dominant paradigm now.

### 2. Unified Multi-Capability Models
Mistral Small 4 sets the template: one model that does instruct, reasoning, vision, and coding. Expect all providers to follow. The days of needing separate models for reasoning vs. chat are ending.

### 3. Hybrid Architectures
NVIDIA's Mamba-2 + MoE + Attention hybrid in Nemotron 3 Super, and Qwen's Gated DeltaNet + Attention hybrid, show that pure Transformer attention is being complemented/replaced by more efficient alternatives, especially for long context.

### 4. "Intelligence Too Cheap to Meter"
MiniMax M2.5's "$1/hour" pricing and the proliferation of Apache 2.0 MoE models are driving cost per intelligence unit to near-zero. Self-hosting competitive models on consumer GPUs is now viable.

### 5. Formal Verification Emerging
Leanstral signals a new category: AI agents that prove their code is correct, not just generate it. This could reshape how we think about code quality for agentic systems.

### 6. Inference Optimization Breakthroughs
Delta-KV compression (video codec concepts applied to KV cache) achieves near-lossless 4-bit KV quantization — potentially transformative for long-context inference on consumer hardware. RYS II shows that simple layer duplication can improve model quality with zero training.

### 7. Community Distillation
Jackrong's Claude Opus reasoning distillations into Qwen3.5 models are extremely popular (141k+ downloads). Knowledge distillation from frontier closed models into smaller open models is a major community trend.

---

## Models to Watch

| Model | Why | Timeline |
|-------|-----|----------|
| Qwen3.5-35B-A3B | Best open MoE for consumer hardware | Available now |
| Nemotron Cascade 2 | 3B active, olympiad-gold reasoning | Available now |
| Mistral Small 4 | Unified model standard-setter | Available now |
| Claude Opus 5 / Sonnet 5 | Next Anthropic generation | Unknown |
| GPT-5 / o3 | Next OpenAI generation | Unknown |
| Gemini 3 | Next Google generation | Unknown |
| Llama 4 | Next Meta open release | Expected 2026 |

---

## Our Hardware Sweet Spot

**Setup:** Mac mini (M-series) + GPU server with 5× RTX 3090 (~120GB VRAM)

**Best fits:**
- **Qwen3.5-35B-A3B (GGUF)** — 3B active, ~20GB quantized, trivially fits
- **Qwen3.5-9B** — Single 3090, daily driver
- **Nemotron Cascade 2 30B-A3B** — 3B active, great for math/code
- **Mistral Small 4 (NVFP4/GGUF)** — 6.5B active but 119B total, needs testing

**Too big:** Nemotron 3 Super (120B), Rakuten 3.0 (671B), MiniMax M2.5 (229B) — use via API

---

## Log

| Date | Notable Events |
|------|---------------|
| 2026-03-24 | Kimi K2.5 recognized as best OS model by Cursor; Delta-KV compression for llama.cpp; RYS II research (layer duplication); Sam Altman exits Helion board, OpenAI eyeing fusion energy; Zuckerberg building AI CEO agent |
| 2026-03-23 | Weekly scan: Mistral Small 4, Leanstral, Nemotron Cascade 2, Nemotron 3 Super, MiniMax M2.5, Rakuten AI 3.0 |
| 2026-03-17 | Mistral Small 4 + Leanstral + Forge launched |
| 2026-03-11 | NVIDIA Nemotron 3 Super released |
| 2026-03-06 | IBM Granite 4.0 1B Speech |
| 2026-02-05 | Claude Opus 4.6 released |
