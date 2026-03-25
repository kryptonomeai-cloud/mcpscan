# Production Guide — TAYoutube

## Recording Setup

### Camera Angles (2 minimum)
1. **Main (face cam):** Slightly above eye level, well-lit face, blurred background showing tech/hardware
2. **Screen capture:** OBS or built-in recording, 1080p minimum, 1440p preferred
3. **B-roll (optional but impactful):** Close-ups of hardware, typing, cable management, LED glow

### Audio (THIS MATTERS MORE THAN VIDEO)
- External mic (USB condenser or lavalier) — NOT laptop mic
- Record audio separately if possible (sync in post)
- Room treatment: even a blanket behind the monitor helps
- Test: record 10 seconds, play back. If it sounds echoey or tinny, fix before filming

### Lighting
- Key light: Ring light or LED panel, 45° from face
- Accent: RGB strips on hardware (blue/green glow = tech aesthetic)
- Avoid: overhead fluorescent, backlit windows

### Software
- **Recording:** OBS Studio (free, handles screen + webcam + audio)
- **Editing:** DaVinci Resolve (free tier is excellent) or CapCut (faster for Shorts)
- **Thumbnails:** Canva (fast) or Figma (precise)
- **Screen recording:** OBS or built-in OS recorder

---

## Editing Style (Study Your Inspirations)

### NetworkChuck Style
- Fast cuts (no dead air)
- Zoom-ins on key moments
- Pop-up text for emphasis
- Sound effects (subtle — keyboard clicks, whoosh on transitions)
- Face cam in corner during screen shares

### Jakkuh Style
- Clean, minimal
- Smooth transitions
- Typography-heavy (animated text overlay)
- Colour-graded for consistency

### Gabriel VIP Style
- Dark, moody aesthetic
- Neon accent colours
- Quick cuts, meme inserts
- Music-driven pacing

### YOUR Style (develop over time)
- Start with NetworkChuck energy (proven formula)
- Add UK personality (dry humour, understatement)
- Lean into the "building" aesthetic — show hardware, terminals, real infrastructure
- Keep it real — show mistakes, troubleshooting, "well that didn't work"

---

## Editing Checklist

- [ ] Hook in first 5 seconds (or viewers leave)
- [ ] Remove ALL dead air and "ums"
- [ ] Add captions/subtitles (auto-generate, then fix errors)
- [ ] Background music (lo-fi, tech ambient — low volume, just texture)
- [ ] Zoom/pan on important screen areas
- [ ] Face cam visible when explaining (trust = face)
- [ ] End screen: subscribe button + next video card
- [ ] Total runtime: 8-15 min for long-form, 30-60 sec for Shorts

---

## Upload Checklist

### Title (Most Important After Thumbnail)
- **Format:** "I [did thing] (result)" or "How to [achieve thing] in [timeframe]"
- Front-load the interesting part
- Include ONE keyword (AI, homelab, Docker, etc.)
- NO clickbait that doesn't deliver — trust is everything
- 50-60 characters ideal (full visibility on mobile)

### Description (SEO goldmine)
```
First 2 lines: What this video is about (shows in search)

⏱ Timestamps:
0:00 - Intro
0:30 - [Section]
...

🔗 Links mentioned:
- [Tool name]: https://...

📱 Follow me:
- Twitter: @...
- GitHub: ...

🏷 Tags: (YouTube studio, not description)
```

### Tags (15-20 per video)
- Mix of broad ("AI tutorial") and specific ("LoRA fine-tuning RTX 3090")
- Include your name for brand search
- Include competitor names (people searching them might find you)

### Thumbnail
- Upload CUSTOM thumbnail (never use auto-generated)
- A/B test with different versions after 48 hours if CTR is low
- Target CTR: 4-6% minimum, 8%+ is excellent

---

## Shorts-Specific Tips

- **Vertical (9:16)** — film separate or crop from landscape
- **Hook in frame 1** — text overlay or visual shock
- **Loop-friendly** — make the ending lead back to the start
- **No intro** — jump straight to content
- **Caption EVERYTHING** — most people watch without sound
- **Trending audio** — use if relevant, but tech content doesn't need it

---

## Workflow: Idea → Published Video

### Day 1: Research & Script
1. Run `scripts/trend-scanner.sh` 
2. Pick topic from ideas backlog
3. Write script using `templates/video-script-template.md`
4. Outline B-roll shots needed

### Day 2: Film
1. Set up recording (camera, audio, lighting, OBS)
2. Film intro/hook LAST (after you're warmed up)
3. Screen record the build/tutorial
4. Film face cam reactions and explanations
5. Capture B-roll (hardware close-ups, typing shots)

### Day 3: Edit & Upload
1. Rough cut: assemble clips in order
2. Fine cut: remove dead air, add zooms/text
3. Polish: music, captions, colour grade
4. Export: 1080p/1440p, high bitrate
5. Create thumbnail
6. Write title/description/tags
7. Upload, schedule for optimal time (see GROWTH-PLAN.md)
8. Cut 2-3 Shorts from the long-form footage

---

## Music & Sound Effects (Copyright-Safe)

- **Epidemic Sound** (£13/mo — huge library, YouTube-safe)
- **Artlist** (yearly sub — unlimited use)
- **YouTube Audio Library** (free, limited but safe)
- **Uppbeat** (free tier available)

For sound effects: freesound.org (free, CC licensed)
