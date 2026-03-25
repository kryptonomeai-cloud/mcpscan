# Video Script: "I Built a 120GB VRAM AI Server (5x RTX 3090)"

**Date:** Week 1
**Pillar:** Hardware + AI
**Target length:** 12-15 minutes
**Primary keyword:** "RTX 3090 AI server build", "GPU server homelab"
**Thumbnail concept:** You standing next to the open server, all 5 GPUs glowing + "120GB VRAM" in large text + your excited face

---

## Why This Video

- Hardware builds ALWAYS perform well (Jeff Geerling, Linus)
- "5x RTX 3090" is a clickable flex
- Sets up every future AI video ("remember that server I built?")
- Evergreen: people will search "GPU server build" for years
- Your unique asset — most AI YouTubers rent cloud GPUs

---

## Hook (0-15 seconds)

> *[Wide shot: walk up to the server, LEDs glowing]*
> 
> "This machine has 120 gigabytes of VRAM, five RTX 3090s, and it cost me less than a single cloud GPU subscription over two years. Let me show you what it can do."

---

## Context (30 seconds)

> "If you're running AI models locally — LLMs, image generation, fine-tuning — you need GPU memory. Lots of it. Cloud GPUs cost a fortune. So I built my own."
>
> Show price comparison: AWS p4d instance (~$32/hr) vs this build total cost

---

## The Build

### Segment 1: The Hardware Specs (2 min)
**Show:** Each component up close
- ThinkStation P620 (Threadripper platform)
- 5x RTX 3090 (24GB each = 120GB total)
- 125GB system RAM
- 1.8TB NVMe + 2TB storage drive
- Total cost breakdown on screen

**B-roll:** Unboxing shots, GPU installation, cable management (or lack thereof)

### Segment 2: What 120GB VRAM Actually Gives You (3 min)
**Demo on camera:**
- Running Qwen 32B (20GB VRAM) — real-time chat
- Running Llama 70B quantised across GPUs
- Running 122B parameter model (Qwen 3.5 122B)
- Image generation with ComfyUI (Wan 2.2 video generation)
- Training a LoRA adapter (live `nvidia-smi` showing all GPUs working)

**Key stat:** "Right now, this machine is running an autonomous AI researcher that trains neural networks while I sleep. It's been running experiments for 19 hours straight."

### Segment 3: Software Stack (2 min)
**Screen recording:**
- Ollama serving models
- ComfyUI for image/video generation
- Training infrastructure (unsloth, PyTorch)
- Monitoring (nvidia-smi, btop)

### Segment 4: The Cost Breakdown (2 min)
**On screen:** Spreadsheet/graphic
- Each component + price paid (used market vs new)
- Monthly electricity cost
- Compare to: Cloud GPU pricing over 12 months
- "Break-even point: X months"
- "After that, it's essentially free AI compute forever"

### Segment 5: Mistakes & Lessons (1.5 min)
**Face cam, honest:**
- Power requirements (multi-GPU power draw)
- Cooling (5 GPUs = a space heater)
- Multi-GPU training gotchas (DDP vs model sharding)
- "If I built this again, I'd change..."

### Segment 6: What I Run On It Daily (1.5 min)
**Montage:**
- Email classification model (custom LoRA)
- ComfyUI image generation
- Ollama for local LLM chat
- Autonomous research experiments
- Video generation (Wan 2.1/2.2)

---

## Payoff (30 seconds)

> *[nvidia-smi showing all 5 GPUs lit up]*
> "Five GPUs, 120 gigs of VRAM, running 24/7. Everything from chatbots to video generation to training custom models — all local, all private, zero API costs."

---

## Outro (15 seconds)

> "Next video: I'll show you how to actually SET UP one of these — the software stack, the models, everything you need to go from bare metal to running AI. Subscribe so you don't miss it."

---

## Shorts Opportunities

1. [ ] "This server has 120GB of VRAM" — 30 sec: hardware reveal + nvidia-smi
2. [ ] "How much does a home GPU server cost?" — 45 sec: price breakdown
3. [ ] "Cloud GPUs vs Building Your Own" — 30 sec: cost comparison
4. [ ] "Watch this AI generate a video locally" — 45 sec: Wan 2.2 demo

---

## Pre-Film Checklist

- [ ] Server clean and presentable (cable management, LEDs on)
- [ ] nvidia-smi showing all 5 GPUs
- [ ] Cost spreadsheet prepared
- [ ] Demo models pre-loaded (Qwen 32B, ComfyUI workflow ready)
- [ ] Good lighting on the hardware (LED strips help)
- [ ] Wide shot + close-up shots of GPUs
