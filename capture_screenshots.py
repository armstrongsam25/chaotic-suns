"""Capture multiple screenshots for itch.io store page."""
import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import sys
sys.path.insert(0, '.')
from src.nbody import create_three_body_system, create_planet
from src.renderer import Renderer
from src.civilization import Civilization
from src.lore import LoreEngine
from src.starfield import Starfield
from src.effects import NebulaRenderer
from src.fleet import FleetManager, SpaceProbe
from src.menu import Menu
from src.tech_tree import TechManager, TechTreeDisplay, TECH_TREE as TT
from src.events import EventManager
from src.effects import ShockwaveEffect, ScreenShake, TransitionEffect

def capture(name, fn):
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.NOFRAME)
    fn(screen)
    pygame.image.save(screen, name)
    print(f"  ✓ {name} ({os.path.getsize(name)} bytes)")
    pygame.quit()

def shot_gameplay(screen):
    """Main gameplay with probes and effects."""
    W, H = 1200, 800
    renderer = Renderer(screen)
    sim = create_three_body_system('default')
    planet = create_planet(sim, pos=(100, 100), vel=(0, 30), name="Chaos Prime")
    civ = Civilization()
    starfield = Starfield(W, H, 300)
    nebula = NebulaRenderer(W, H)
    fleet = FleetManager()

    for i in range(80):
        sim.step(0.15)
        stability = sim.get_stability_metric()
        civ.update(stability, 0.02)

    fleet.build('scout', planet.pos, sim, civ, target_body=0)
    civ.knowledge = 30
    fleet.unlock_tech(30)
    fleet.build('observer', planet.pos, sim, civ, target_body=1)

    for _ in range(10):
        sim.step(0.1)
        fleet.update(sim, 0.1)

    starfield.update(0.5, 0.3)
    starfield.draw(screen)
    nebula.draw(screen, camera_offset=renderer.camera.offset)
    renderer.render(sim, civ.current_era, sim.get_stability_metric(),
                    civ.population, 'observe', 1.0, False)
    fleet.draw(screen, renderer.camera)

    # HUD
    font = pygame.font.Font(None, 20)
    planet_idx = len(sim.bodies) - 1
    temp = sim.get_planet_temperature(planet_idx)
    temp_color = (255, 150, 50) if temp > 40 else (200, 200, 100)
    screen.blit(font.render(f"Temp: {temp:.0f}°C", True, temp_color), (10, 50))
    screen.blit(font.render(f"Era: STABLE", True, (100, 255, 100)), (10, 10))
    screen.blit(font.render(f"Knowledge: {civ.knowledge:.0f}%", True, (100, 200, 255)), (W - 200, 10))
    screen.blit(font.render(f"Population: {civ.population:.0f}", True, (255, 255, 255)), (W - 200, 35))

def shot_menu(screen):
    """Main menu screen."""
    W, H = 1200, 800
    starfield = Starfield(W, H, 300)
    starfield.update(0.5, 0.3)
    starfield.draw(screen)

    font_large = pygame.font.Font(None, 72)
    font_med = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 22)

    title = font_large.render("CHAOTIC SUNS", True, (255, 215, 0))
    subtitle = font_med.render("Survive the patterns, or die trying.", True, (200, 200, 200))

    screen.blit(title, (W//2 - title.get_width()//2, H//2 - 120))
    screen.blit(subtitle, (W//2 - subtitle.get_width()//2, H//2 - 50))

    menu_items = [
        ("[ ENTER ]  Start Game", (255, 255, 100)),
        ("[ S ]      Scenarios", (180, 180, 180)),
        ("[ A ]      Achievements", (180, 180, 180)),
        ("[ H ]      Help / Controls", (180, 180, 180)),
        ("[ ESC ]    Quit", (180, 180, 180)),
    ]

    y = H//2 + 20
    for text, color in menu_items:
        item = font_med.render(text, True, color)
        screen.blit(item, (W//2 - item.get_width()//2, y))
        y += 40

    hint = font_small.render("v0.2.0-beta — free cosmic survival sim", True, (120, 120, 120))
    screen.blit(hint, (W//2 - hint.get_width()//2, H - 40))

def shot_research(screen):
    """Research/tech tree screen."""
    W, H = 1200, 800
    starfield = Starfield(W, H, 200)
    starfield.update(0.5, 0.3)
    starfield.draw(screen)

    civ = Civilization()
    civ.knowledge = 45
    civ.total_cycles = 10

    tm = TechManager()
    display = TechTreeDisplay(W, H)
    display.setup(TT, civ.knowledge, set())
    display.render(screen)

def shot_prediction(screen):
    """Prediction mode with drawn paths."""
    W, H = 1200, 800
    renderer = Renderer(screen)
    sim = create_three_body_system('default')
    planet = create_planet(sim, pos=(100, 100), vel=(0, 30), name="Chaos Prime")
    civ = Civilization()
    starfield = Starfield(W, H, 300)
    nebula = NebulaRenderer(W, H)

    for _ in range(60):
        sim.step(0.15)

    starfield.update(0.5, 0.3)
    starfield.draw(screen)
    nebula.draw(screen, camera_offset=renderer.camera.offset)
    renderer.render(sim, civ.current_era, sim.get_stability_metric(),
                    civ.population, 'predict', 1.0, False)

    font = pygame.font.Font(None, 20)
    hint = font.render("PREDICTION MODE — Draw orbits with mouse", True, (255, 215, 0))
    screen.blit(hint, (W//2 - hint.get_width()//2, 10))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    captures = [
        ("screenshot_menu.png", shot_menu),
        ("screenshot_gameplay.png", shot_gameplay),
        ("screenshot_research.png", shot_research),
        ("screenshot_prediction.png", shot_prediction),
    ]

    print("Capturing screenshots for itch.io...")
    for name, fn in captures:
        capture(name, fn)

    print(f"\nDone! {len(captures)} screenshots in {os.getcwd()}/")