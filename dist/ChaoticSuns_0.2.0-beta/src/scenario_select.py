"""Scenario and difficulty selection screen."""

import pygame
from src.constants import *
from src.progression import SCENARIOS, DIFFICULTY_SETTINGS, Difficulty


class ScenarioSelectScreen:
    """Screen for selecting scenario and difficulty."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.title_font = pygame.font.Font(None, 42)
        self.body_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.scenario_buttons = []
        self.difficulty_buttons = []
        self.back_button = None
        self.start_button = None
        self.selected_scenario = None
        self.selected_difficulty = None

    def setup(self, progression):
        """Setup with unlocked scenarios from progression."""
        cx = self.width // 2
        unlocked = progression.unlocked_scenarios

        # Scenario buttons
        self.scenario_buttons = []
        start_y = 120
        for i, scenario in enumerate(SCENARIOS):
            if scenario['id'] in unlocked:
                btn = {
                    'rect': pygame.Rect(cx - 300, start_y + i * 65, 600, 55),
                    'scenario': scenario,
                    'unlocked': True,
                }
            else:
                btn = {
                    'rect': pygame.Rect(cx - 300, start_y + i * 65, 600, 55),
                    'scenario': scenario,
                    'unlocked': False,
                }
            self.scenario_buttons.append(btn)

        # Difficulty buttons
        diff_y = start_y + len(SCENARIOS) * 65 + 40
        self.difficulty_buttons = []
        diff_options = [Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD, Difficulty.IMPOSSIBLE]
        diff_labels = ["Easy", "Normal", "Hard", "Impossible"]
        for i, diff in enumerate(diff_options):
            btn = {
                'rect': pygame.Rect(cx - 230 + i * 120, diff_y, 105, 40),
                'difficulty': diff,
                'settings': DIFFICULTY_SETTINGS[diff],
                'selected': progression.current_difficulty == diff,
            }
            self.difficulty_buttons.append(btn)

        self.selected_scenario = progression.current_scenario
        self.selected_difficulty = progression.current_difficulty

        # Start button
        self.start_button = pygame.Rect(cx - 100, self.height - 100, 200, 45)

        # Back button
        self.back_button = pygame.Rect(cx - 100, self.height - 45, 200, 35)

    def update(self, mouse_pos, mouse_click):
        """Handle input, return action."""

        # Check scenario buttons
        for btn in self.scenario_buttons:
            if btn['unlocked'] and btn['rect'].collidepoint(mouse_pos) and mouse_click:
                self.selected_scenario = btn['scenario']

        # Check difficulty buttons
        for btn in self.difficulty_buttons:
            if btn['rect'].collidepoint(mouse_pos) and mouse_click:
                self.selected_difficulty = btn['difficulty']
                for b in self.difficulty_buttons:
                    b['selected'] = (b['difficulty'] == btn['difficulty'])

        # Start button
        if self.start_button and self.start_button.collidepoint(mouse_pos) and mouse_click:
            return "start"

        # Back button
        if self.back_button and self.back_button.collidepoint(mouse_pos) and mouse_click:
            return "back"

        return None

    def render(self, surface):
        """Render the scenario select screen."""
        # Background
        surface.fill(DARK_BLUE)
        for y in range(self.height):
            t = y / self.height
            color = (int(5 + 10 * t), int(5 + 5 * t), int(25 + 20 * t))
            pygame.draw.line(surface, color, (0, y), (self.width, y))

        # Title
        title = self.title_font.render("SELECT SCENARIO", True, YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 40))
        surface.blit(title, title_rect)

        subtitle = self.small_font.render(
            "Choose your initial conditions and difficulty", True, GRAY
        )
        sub_rect = subtitle.get_rect(center=(self.width // 2, 75))
        surface.blit(subtitle, sub_rect)

        # Scenario buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.scenario_buttons:
            rect = btn['rect']
            scenario = btn['scenario']
            hovered = rect.collidepoint(mouse_pos) and btn['unlocked']
            selected = self.selected_scenario and self.selected_scenario['id'] == scenario['id']

            # Button background
            if not btn['unlocked']:
                color = (30, 30, 50)
                border = (50, 50, 70)
            elif selected:
                color = (40, 60, 100)
                border = YELLOW
            elif hovered:
                color = (50, 50, 90)
                border = CYAN
            else:
                color = (35, 35, 60)
                border = (60, 60, 80)

            pygame.draw.rect(surface, color, rect, border_radius=5)
            pygame.draw.rect(surface, border, rect, 2, border_radius=5)

            # Name
            name = scenario['name'] if btn['unlocked'] else "??? (Locked)"
            name_text = self.body_font.render(name, True, WHITE if btn['unlocked'] else DARK_GRAY)
            surface.blit(name_text, (rect.x + 15, rect.y + 8))

            # Description
            desc = scenario['description'] if btn['unlocked'] else "Complete previous scenarios to unlock"
            desc_text = self.small_font.render(desc, True, GRAY if btn['unlocked'] else DARK_GRAY)
            surface.blit(desc_text, (rect.x + 15, rect.y + 30))

            # Lock icon
            if not btn['unlocked']:
                lock = self.body_font.render("🔒", True, DARK_GRAY)
                surface.blit(lock, (rect.right - 40, rect.y + 15))

        # Difficulty section
        diff_label = self.body_font.render("DIFFICULTY:", True, CYAN)
        diff_x = self.width // 2 - diff_label.get_width() // 2
        diff_y = self.difficulty_buttons[0]['rect'].y - 25
        surface.blit(diff_label, (diff_x, diff_y))

        for btn in self.difficulty_buttons:
            rect = btn['rect']
            hovered = rect.collidepoint(mouse_pos)

            if btn['selected']:
                color = (40, 80, 140)
                border = YELLOW
            elif hovered:
                color = (60, 60, 100)
                border = CYAN
            else:
                color = (35, 35, 60)
                border = (60, 60, 80)

            pygame.draw.rect(surface, color, rect, border_radius=5)
            pygame.draw.rect(surface, border, rect, 2, border_radius=5)

            name = btn['settings']['name']
            name_text = self.small_font.render(name, True, WHITE)
            name_rect = name_text.get_rect(center=rect.center)
            surface.blit(name_text, name_rect)

        # Selected difficulty description
        if self.selected_difficulty:
            settings = DIFFICULTY_SETTINGS[self.selected_difficulty]
            desc_text = self.small_font.render(
                settings['description'], True, GRAY
            )
            desc_rect = desc_text.get_rect(center=(self.width // 2, diff_y + 65))
            surface.blit(desc_text, desc_rect)

        # Start button
        start_hovered = self.start_button.collidepoint(mouse_pos)
        start_color = (40, 120, 60) if start_hovered else (30, 80, 40)
        pygame.draw.rect(surface, start_color, self.start_button, border_radius=5)
        pygame.draw.rect(surface, GREEN if start_hovered else (60, 100, 60),
                         self.start_button, 2, border_radius=5)
        start_text = self.body_font.render("BEGIN SIMULATION", True, WHITE)
        start_rect = start_text.get_rect(center=self.start_button.center)
        surface.blit(start_text, start_rect)

        # Back button
        back_hovered = self.back_button.collidepoint(mouse_pos)
        back_color = (80, 40, 40) if back_hovered else (50, 30, 30)
        pygame.draw.rect(surface, back_color, self.back_button, border_radius=5)
        pygame.draw.rect(surface, RED if back_hovered else (80, 50, 50),
                         self.back_button, 2, border_radius=5)
        back_text = self.small_font.render("BACK TO MENU", True, WHITE)
        back_rect = back_text.get_rect(center=self.back_button.center)
        surface.blit(back_text, back_rect)