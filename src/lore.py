"""Narrative lore system with original quotes and events."""

import random


ORIGINAL_QUOTES = [
    "In the dance of three suns, only the patient survive.",
    "A stable era is a gift. A chaotic era is a lesson.",
    "We looked to the heavens and found only uncertainty.",
    "Civilizations rise like waves, and fall like them too.",
    "The ancients recorded 192 civilizations. Only the 193rd learned to watch the patterns.",
    "Knowledge is the only shield against the chaos.",
    "To a civilization of the three suns, a single sunrise is a miracle.",
    "The astronomers said it was impossible. The mathematicians proved them right.",
    "We are small. The universe is vast. And chaos has no mercy.",
    "Between the burning and the freezing, there is a narrow band called hope.",
    "They say the universe is empty. We know better — the universe is watching.",
    "A prediction is not certainty. It is a bet against chaos.",
    "The probe was launched on a Tuesday. By Friday, it had seen three sunrises.",
    "Some say the stars are random. Others say they are merely complicated.",
    "The old ones knew: when the sky turns orange, dig deep.",
]

ERA_TRANSITIONS = {
    "stable": [
        "A golden age dawns. The cities rebuild.",
        "For now, the orbits are gentle. The people breathe.",
        "The libraries fill with knowledge. Scholars study the heavens.",
        "A rare alignment brings warmth and hope.",
        "Crops grow. Children play under a calm sky.",
    ],
    "chaotic": [
        "The suns dance wildly. Civilization holds its breath.",
        "Chaos returns. The old fears resurface.",
        "A sun grows too close. The ground trembles.",
        "The sky turns to fire and ice in the same hour.",
        "A dark era begins. The people take shelter.",
    ],
    "transition": [
        "Something is changing. The patterns are shifting.",
        "The astronomers argue. No one knows what comes next.",
        "A tension hangs in the air. The suns are indecisive.",
        "Between eras, there is only uncertainty.",
    ],
}

MILESTONE_NARRATIVES = {
    "first_cycle": "100 cycles of watching the skies! The astronomers have recorded their first complete pattern. Is it repeatable? Only time will tell.",
    "stable_era_100": "A century of stability! The people call this the Golden Century. Art, science, and culture flourish under a calm sky.",
    "population_max": "The planet teems with life. Cities span the continents. For this brief moment, civilization is at its zenith.",
    "survive_10_collapses": "Ten civilizations have risen and fallen on this world. Each collapse left lessons behind. The people have learned resilience beyond measure.",
    "knowledge_50": "You begin to see the patterns beneath the chaos. The suns are not random — their movements follow laws. A solution may exist...",
    "knowledge_100": "ENLIGHTENMENT. You have glimpsed the underlying order of the chaotic system. The civilization now has a chance to predict, to prepare, to survive.",
    "first_prediction": "You've made your first prediction. The path ahead shimmers with possibility and uncertainty.",
    "predict_era_change": "You correctly predicted an era change! Your understanding of the patterns grows deeper.",
    "first_probe": "First probe launched! The people look to the stars with new hope.",
    "fleet_commander": "Fleet Commander! Five probes are now active among the suns. The civilization reaches outward.",
}


class LoreEngine:
    """Generates narrative flavor and events."""

    def __init__(self):
        self.current_quote = None
        self.quote_timer = 0
        self.quote_duration = 300  # Frames between quote changes

    def update(self, dt, current_era, stability, knowledge):
        """Update lore state."""
        self.quote_timer -= dt
        if self.quote_timer <= 0:
            self.current_quote = self.get_random_quote()
            self.quote_timer = self.quote_duration + random.uniform(-60, 60)

    def get_random_quote(self):
        return random.choice(ORIGINAL_QUOTES)

    def get_era_narrative(self, era):
        """Get flavor text for an era transition."""
        choices = ERA_TRANSITIONS.get(era, ERA_TRANSITIONS["transition"])
        return random.choice(choices)

    def get_milestone_narrative(self, milestone_id):
        """Get narrative text for a milestone."""
        return MILESTONE_NARRATIVES.get(milestone_id)

    def get_active_quote(self):
        """Return the current active quote for display."""
        return self.current_quote