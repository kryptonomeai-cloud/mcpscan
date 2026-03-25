# Video Script: "Running AI Locally — The REAL Guide (No Cloud, No API Keys)"

**Date:** Week 1-2
**Pillar:** AI
**Target length:** 10-12 minutes
**Primary keyword:** "run AI locally", "local LLM setup", "ollama tutorial"
**Thumbnail concept:** Your face (confident) + laptop with glowing terminal + "NO CLOUD NEEDED" in bold

---

## Hook (0-10 seconds)

> *[Screen: terminal, model responding in real-time]*
> "This AI model is running entirely on my machine. No API keys, no cloud, no monthly bill, and nobody can see what I'm asking it. Here's how to set it up in under 5 minutes."

---

## Context (30 seconds)

> "Every AI tutorial tells you to sign up for OpenAI, get an API key, and start paying per token. But what if I told you the best open source models are now genuinely competitive — and you can run them for free, right now, on hardware you already own?"

---

## The Build

### Step 1: Install Ollama (1.5 min)
**Screen:** Terminal
- One-line install: `curl -fsSL https://ollama.ai/install.sh | sh`
- Windows/Mac: download from website
- "That's it. You now have a local AI runtime."
- Pull first model: `ollama pull qwen2.5:7b`
- Show it downloading, explain what quantisation means (briefly)

### Step 2: Your First Conversation (1.5 min)
**Screen:** Terminal chat
- `ollama run qwen2.5:7b`
- Ask it something genuinely useful (not "hello world")
- "Write me a Python script that monitors my CPU temperature"
- Show it working — highlight speed, quality
- Compare to ChatGPT response side-by-side

### Step 3: Which Model For What (2 min)
**Screen:** Comparison table/graphic
- **Coding:** Qwen 2.5 Coder, DeepSeek Coder
- **General chat:** Llama 3.3, Qwen 3
- **Small & fast:** Phi-3, Gemma 2
- **Reasoning:** Qwen 3 32B (if you have the VRAM)
- Show VRAM requirements for each
- "Don't have a GPU? These models run on CPU too — just slower."

### Step 4: Making It Actually Useful (2 min)
**Screen:** Various demos
- **Open WebUI:** Beautiful ChatGPT-like interface for Ollama
  - `docker run -p 3000:8080 ghcr.io/open-webui/open-webui:main`
  - Show the UI, multiple conversations, model switching
- **IDE integration:** Continue.dev or Cody in VS Code
  - Show autocomplete powered by local model
- **API access:** `curl http://localhost:11434/api/generate`
  - Build your own tools on top

### Step 5: Performance Tips (1.5 min)
**Screen:** nvidia-smi + benchmarks
- GPU vs CPU: show tokens/second difference
- Context length matters: explain what it means practically
- "If your model is slow, try a smaller quantisation: Q4_K_M is the sweet spot"
- Keep models warm: `keep_alive` setting

### Step 6: Privacy & Why This Matters (1 min)
**Face cam:**
- "Everything stays on your machine. No data sent anywhere."
- Company policies that ban external AI? Run it locally.
- Sensitive documents? Ask your LOCAL model.
- "This isn't just about saving money. It's about control."

---

## Payoff (30 seconds)

> *[Show Open WebUI with multiple conversations]*
> "You now have a private AI assistant that costs nothing to run, works offline, and keeps everything local. No subscriptions, no API limits, no one reading your prompts."

---

## Outro (15 seconds)

> "In the next video, I'll show you the server I built to run the REALLY big models — 70 billion parameters and above. If you want to see what happens when you throw five GPUs at AI, subscribe."

---

## Shorts

1. [ ] "Install AI on your computer in 60 seconds" — Ollama install + first prompt
2. [ ] "This free AI runs on YOUR laptop" — Side-by-side with ChatGPT
3. [ ] "Stop paying for AI" — Cost comparison
4. [ ] "The AI setup nobody talks about" — Open WebUI reveal

## SEO Tags
ollama, local llm, run ai locally, local ai setup, open source ai, llama local, qwen local, no api key ai, self hosted ai, ollama tutorial 2026, private ai, local chatgpt alternative, open webui
