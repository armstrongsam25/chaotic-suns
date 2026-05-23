# 🌌 Chaotic Suns

A cosmic survival game where you guide a civilization orbiting unpredictable suns. Observe, predict, and survive the chaos.

~4,700 lines of Python code. Built from scratch.

## 🎮 Gameplay

You find yourself on **Chaos Prime**, a planet orbiting three suns in an unpredictable, chaotic pattern. Civilizations rise and fall as the eras shift between Stable (predictable) and Chaotic (deadly). Your goal: observe, predict, and guide civilization toward understanding the n-body chaos.

### Core Mechanics

- **Orbital Observation** — Watch the suns dance. Study their patterns.
- **Prediction Mode** — Draw predicted orbital paths and earn accuracy scores (E key)
- **Civilization Management** — Grow your population during Stable Eras, hunker down during Chaos
- **Knowledge System** — Accumulate understanding, unlock discoveries, earn milestones
- **Tech Tree** — 10 researchable technologies from basic survival to n-body solution
- **Space Fleet** — Build and launch 4 types of probes to explore the system
- **Random Events** — 6 event types: solar flares, gravitational spikes, meteor showers, and more
- **Difficulty Scaling** — 4 levels from "Stable Observer" to "Event Horizon"

### Features

- ⚛️ **N-body Physics** — Velocity Verlet integration with realistic gravitational forces
- 🌡️ **Planet Temperature** — Your planet heats up near suns and freezes in deep space
- 💥 **Sun Collisions** — When suns get too close: particle effects, shockwaves, screen shake
- 🎨 **Visual Effects** — Nebula clouds, multi-layer parallax starfield, bloom, scanlines, vignette
- 📜 **Lore System** — Original narrative quotes and era flavor text
- 🏆 **10 Achievements** — Unlock milestones from "First Cycle" to "Enlightenment"
- 🎬 **4 Scenarios** — Classic System, Figure-Eight, Tight Embrace, Vast Expanse
- 💾 **Save/Load** — Quick save (F5) and quick load (F9)
- 🚀 **Space Probes** — Scout, Deep Observer, Sun Diver, Interstellar Ark
- ⚡ **Random Events** — Solar Flares, Gravitational Spikes, Syzygies, and more
- 🔬 **Tech Tree** — 10 technologies with prerequisites and permanent buffs

## 🚀 Running

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Play
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| Space | Pause / Resume |
| E | Toggle Prediction Mode |
| R | Reset Simulation |
| H | Toggle Help |
| T | Research Lab (tech tree) |
| Tab | Toggle Event Log |
| M | Mute / Unmute |
| F5 / F9 | Quick Save / Load |
| F | Fullscreen |
| 0 / 1 / 2 / 5 | Set Time Speed (paused / 1× / 2× / 5×) |
| [ / ] | Fine-tune Time Scale |
| + / - | Zoom In / Out |
| Arrow Keys | Pan View |
| Mouse Drag / Scroll | Pan / Zoom |
| 1-4 | Launch Probes |
| Left Click | Draw prediction path (in Predict mode) |
| Right Click | Pan (in Predict mode) |
| Esc | Menu / Quit |

## 🏗️ Architecture

```
chaotic-suns/
├── main.py              # Game loop, state machine, input handling
├── src/
│   ├── nbody.py         # N-body physics engine (Velocity Verlet)
│   ├── renderer.py      # Camera, sun glow, orbit trails, VR effects
│   ├── civilization.py  # Population, era tracking, collapse system
│   ├── prediction.py    # Orbital prediction overlay & knowledge discovery
│   ├── effects.py       # Nebula, shockwaves, screen shake, transitions
│   ├── starfield.py     # Multi-layer parallax starfield & bloom
│   ├── progression.py   # Difficulty levels, scenario management
│   ├── menu.py          # Main menu & pause menu screens
│   ├── scenario_select.py  # Scenario/difficulty selection screen
│   ├── achievements.py  # Achievements & stats display
│   ├── audio.py         # Procedural audio generation
│   ├── lore.py          # Original narrative quotes & flavor text
│   ├── save_system.py   # JSON save/load system
│   ├── fleet.py         # Space probe system (4 probe types)
│   ├── events.py        # Random event system (6 event types)
│   ├── tech_tree.py     # Tech tree with 10 technologies
│   └── constants.py     # Physics constants, colors, config
└── requirements.txt
```

## 🛠️ Tech Stack

- Python 3.12+
- Pygame 2.6+ (rendering, input)
- NumPy (physics calculations)

## 📝 Roadmap Ideas

- [ ] Port to Godot for Steam/mobile release
- [ ] GPU-accelerated rendering with ModernGL
- [ ] Multiplayer civilization collaboration
- [ ] More scenarios and initial conditions
- [ ] Advanced prediction tools (freehand drawing, multi-sun)
- [ ] Full soundtrack and audio design
- [ ] Particle effects system overhaul
- [ ] In-app purchase infrastructure

---

*"In the dance of three suns, only the patient survive."*