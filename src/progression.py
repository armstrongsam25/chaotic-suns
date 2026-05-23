"""Game progression, difficulty scaling, and scenario management."""

import random
from enum import Enum
from src.constants import *


class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    IMPOSSIBLE = "impossible"


DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {
        'name': 'Stable Observer',
        'description': 'Favorable initial conditions. The chaos is gentle.',
        'civ_growth_rate': 0.15,
        'civ_death_chaotic': 0.15,
        'civ_death_stable': 0.005,
        'knowledge_rate': 0.08,
        'max_population': 120,
        'collapse_limit': 10,
        'chaos_chance': 0.3,
        'starting_knowledge': 10,
        'starting_population': 70,
    },
    Difficulty.NORMAL: {
        'name': 'Trisolaran Scholar',
        'description': 'Standard chaos. The three-body problem in its full glory.',
        'civ_growth_rate': 0.10,
        'civ_death_chaotic': 0.30,
        'civ_death_stable': 0.01,
        'knowledge_rate': 0.05,
        'max_population': 100,
        'collapse_limit': 3,
        'chaos_chance': 0.5,
        'starting_knowledge': 5,
        'starting_population': 50,
    },
    Difficulty.HARD: {
        'name': 'Chaos Navigator',
        'description': 'The suns are unpredictable. Civilization is fragile.',
        'civ_growth_rate': 0.06,
        'civ_death_chaotic': 0.45,
        'civ_death_stable': 0.015,
        'knowledge_rate': 0.03,
        'max_population': 80,
        'collapse_limit': 1,
        'chaos_chance': 0.7,
        'starting_knowledge': 0,
        'starting_population': 30,
    },
    Difficulty.IMPOSSIBLE: {
        'name': 'Dark Forest',
        'description': 'The true Trisolaran experience. Good luck.',
        'civ_growth_rate': 0.03,
        'civ_death_chaotic': 0.60,
        'civ_death_stable': 0.02,
        'knowledge_rate': 0.01,
        'max_population': 60,
        'collapse_limit': 0,
        'chaos_chance': 0.85,
        'starting_knowledge': 0,
        'starting_population': 15,
    },
}

SCENARIOS = [
    {
        'id': 'default',
        'name': 'Classic Trisolaris',
        'description': 'The standard three-sun system. Three suns of varying mass orbit in a beautiful, chaotic dance.',
        'config': 'default',
        'planet_pos': (100, 100),
        'planet_vel': (0, 30),
        'recommended': Difficulty.NORMAL,
    },
    {
        'id': 'figure8',
        'name': 'The Eternal Figure-Eight',
        'description': 'A rare stable configuration discovered by mathematicians. Three equal-mass suns trace a perfect figure-eight. But even stable orbits can be disrupted...',
        'config': 'figure8',
        'planet_pos': (80, -50),
        'planet_vel': (15, 5),
        'recommended': Difficulty.EASY,
    },
    {
        'id': 'close',
        'name': 'The Tight Embrace',
        'description': 'Three suns born dangerously close. Their gravitational war begins immediately — and Trisolaris is caught in the middle.',
        'config': 'close',
        'planet_pos': (20, 20),
        'planet_vel': (20, -10),
        'recommended': Difficulty.HARD,
    },
    {
        'id': 'wide',
        'name': 'The Vast Expanse',
        'description': 'The suns are far apart. Trisolaris has breathing room — for now. But chaos always finds a way.',
        'config': 'wide',
        'planet_pos': (200, -100),
        'planet_vel': (-5, 20),
        'recommended': Difficulty.NORMAL,
    },
]


class ProgressionManager:
    """Manages game progression, scenarios, and difficulty."""

    def __init__(self):
        self.current_scenario = SCENARIOS[0]
        self.current_difficulty = Difficulty.NORMAL
        self.unlocked_scenarios = {'default', 'figure8'}
        self.best_knowledge = 0
        self.games_played = 0
        self.total_collapses = 0

    def apply_difficulty(self, civilization):
        """Apply difficulty settings to civilization."""
        settings = DIFFICULTY_SETTINGS[self.current_difficulty]
        civilization.max_population = settings['max_population']
        civilization.population = settings['starting_population']
        civilization.knowledge = settings['starting_knowledge']
        civilization.collapse_count = 0
        return settings

    def get_difficulty_effects(self, stability, dt):
        """Get modified rates based on difficulty."""
        settings = DIFFICULTY_SETTINGS[self.current_difficulty]
        growth = settings['civ_growth_rate']
        chaos_death = settings['civ_death_chaotic']
        stable_death = settings['civ_death_stable']
        knowledge_rate = settings['knowledge_rate']
        collapse_limit = settings['collapse_limit']

        # Scale by stability
        if stability < 0.3:  # Chaotic
            actual_growth = 0
            actual_death = chaos_death
            actual_knowledge = 0
        elif stability < 0.6:  # Transition
            actual_growth = growth * 0.5
            actual_death = chaos_death * 0.3
            actual_knowledge = knowledge_rate * 0.5
        else:  # Stable
            actual_growth = growth
            actual_death = stable_death
            actual_knowledge = knowledge_rate

        # Random chaotic events in hard/impossible
        if self.current_difficulty in (Difficulty.HARD, Difficulty.IMPOSSIBLE):
            if random.random() < settings['chaos_chance'] * 0.01 * dt:
                actual_death *= 2.5

        return actual_growth, actual_death, actual_knowledge, collapse_limit

    def select_scenario(self, scenario_id):
        """Select a game scenario."""
        for s in SCENARIOS:
            if s['id'] == scenario_id:
                self.current_scenario = s
                return s
        return SCENARIOS[0]

    def on_game_end(self, knowledge_achieved, collapses_survived):
        """Record end-of-game stats and unlock content."""
        self.games_played += 1
        self.total_collapses += collapses_survived

        if knowledge_achieved > self.best_knowledge:
            self.best_knowledge = knowledge_achieved

        # Unlock scenarios based on achievements
        if knowledge_achieved >= 30:
            self.unlocked_scenarios.add('wide')
        if knowledge_achieved >= 60:
            self.unlocked_scenarios.add('close')
        if self.games_played >= 5:
            self.unlocked_scenarios.add('figure8')

    def get_stats_display(self):
        """Get formatted stats for display."""
        return {
            'games_played': self.games_played,
            'best_knowledge': self.best_knowledge,
            'total_collapses': self.total_collapses,
            'scenarios_unlocked': len(self.unlocked_scenarios),
            'total_scenarios': len(SCENARIOS),
        }