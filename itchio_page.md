# Chaotic Suns — itch.io Page Metadata

## Game Info
title: Chaotic Suns
short_text: Guide a civilization through the chaos of multiple suns. Predict orbits, launch probes, research technologies, and survive.
classification: games
kind: downloadable
price: 0.00
tags:
  - simulation
  - strategy
  - space
  - physics
  - indie
  - 2d
screenshots:
  - url: https://raw.githubusercontent.com/armstrongsam25/chaotic-suns/main/screenshot_gameplay.png
    description: "Main gameplay — Chaos Prime orbiting three suns with active probes"

## Description

🌌 **Chaotic Suns** — A cosmic survival simulation

Your civilization orbits multiple unpredictable suns. The eras shift between Stable (warm, safe) and Chaotic (deadly, unpredictable). Can you survive long enough to understand the patterns?

### What You Do
- **Observe** — Watch the suns' gravitational dance in real-time
- **Predict** — Draw orbital paths and test your accuracy (E key)
- **Build** — Launch space probes to explore the system (keys 1-4)
- **Research** — 10 technologies from basic survival to N-body solution (T key)
- **Survive** — Manage population through era shifts, random events, and collapses

### Features
- ⚛️ Real N-body physics (Velocity Verlet integration)
- 🌡️ Planet temperature & sun proximity system
- 🚀 4 probe types: Scout, Observer, Sun Diver, Interstellar Ark
- 🔬 10-tech research tree with prerequisites
- ⚡ 6 random event types (solar flares, meteor showers, etc.)
- 🏆 10 achievements
- 🎬 4 scenarios + 4 difficulty levels
- 🎨 VR-style visual effects (scanlines, bloom, parallax starfield)
- 💾 Save/load system (F5/F9)

### Requirements
- Python 3.12+
- Windows / macOS / Linux
- 2GB RAM, any GPU

### Install & Run
```bash
python3 -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python3 main.py
```

### Controls
| Key | Action |
|-----|--------|
| Space | Pause/Resume |
| E | Prediction Mode |
| H | Help |
| T | Research Lab |
| 1-4 | Launch Probes |
| Arrow Keys | Pan |
| +/- | Zoom |
| F5/F9 | Quick Save/Load |

### Beta Disclaimer
This is a beta release (v0.2.0). Please send feedback and bug reports!

---

**Repo:** https://github.com/armstrongsam25/chaotic-suns