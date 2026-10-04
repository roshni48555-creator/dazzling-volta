"""
Tarot Deck and Divination Engine for Arcana.
Manages physical deck state, ritual shuffling, interactive cutting,
reversal probabilities, and authentic Tarot spread structures.
"""
import random
from typing import List, Tuple, Optional, Dict, Any
from arcana.cards_data import ALL_CARDS, Card

class DeckOrientationSetting:
    BALANCED = "Balanced (50% Reversals)"
    GENTLE = "Gentle Dawn (25% Reversals)"
    SHADOW = "Shadow Eclipse (75% Reversals)"
    UPRIGHT_ONLY = "Solar Pure (0% Reversals)"

class TarotDeck:
    def __init__(self, reversal_setting: str = DeckOrientationSetting.BALANCED):
        self.cards: List[Card] = list(ALL_CARDS)
        self.reversal_setting = reversal_setting
        self.drawn_history: List[Tuple[Card, bool]] = []
        self.reversal_prob = self._get_prob(reversal_setting)

    def _get_prob(self, setting: str) -> float:
        if setting == DeckOrientationSetting.GENTLE:
            return 0.25
        elif setting == DeckOrientationSetting.SHADOW:
            return 0.75
        elif setting == DeckOrientationSetting.UPRIGHT_ONLY:
            return 0.0
        return 0.50  # Default balanced

    def set_reversal_mode(self, setting: str):
        self.reversal_setting = setting
        self.reversal_prob = self._get_prob(setting)

    def reset_deck(self):
        """Resets the deck with all 78 cards intact."""
        self.cards = list(ALL_CARDS)
        self.drawn_history = []

    def shuffle_riffle(self):
        """Standard riffle shuffle with random reordering."""
        random.shuffle(self.cards)

    def cut_deck(self, cut_depth_fraction: float = 0.5):
        """Splits the deck at a specified depth and transposes the two halves."""
        cut_depth_fraction = max(0.1, min(0.9, cut_depth_fraction))
        cut_point = int(len(self.cards) * cut_depth_fraction)
        top_half = self.cards[:cut_point]
        bottom_half = self.cards[cut_point:]
        self.cards = bottom_half + top_half

    def draw_top(self) -> Tuple[Card, bool]:
        """Draws the top card of the deck with assigned orientation."""
        if not self.cards:
            self.reset_deck()
            self.shuffle_riffle()

        card = self.cards.pop(0)
        is_reversed = (random.random() < self.reversal_prob)
        self.drawn_history.append((card, is_reversed))
        return card, is_reversed

    def draw_by_index(self, index: int) -> Tuple[Card, bool]:
        """Draws a card selected by index (0-based) from available cards."""
        if not self.cards:
            self.reset_deck()
            self.shuffle_riffle()
            
        index = index % len(self.cards)
        card = self.cards.pop(index)
        is_reversed = (random.random() < self.reversal_prob)
        self.drawn_history.append((card, is_reversed))
        return card, is_reversed

# Spread definitions
SPREAD_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "single": {
        "id": "single",
        "name": "The Single Mirror (Oracle's Whisper)",
        "card_count": 1,
        "description": "A laser-focused reading revealing the dominant celestial energy of the moment.",
        "positions": [
            ("The Central Eye", "The core truth, current climate, or direct answer to your question.")
        ]
    },
    "trinity": {
        "id": "trinity",
        "name": "The Trinity of Time (Past, Present, Future)",
        "card_count": 3,
        "description": "Chronicles the arc of your timeline: origins, current crucible, and the horizon ahead.",
        "positions": [
            ("The Roots (Past)", "Karmic foundations, past choices, and origin energies."),
            ("The Crucible (Present)", "Current situation, active challenges, and immediate reality."),
            ("The Dawn (Future)", "Likely trajectory, emerging opportunity, and eventual harvest.")
        ]
    },
    "mind_heart_spirit": {
        "id": "mind_heart_spirit",
        "name": "The Triad of Mind, Heart & Soul",
        "card_count": 3,
        "description": "Aligns your three internal compasses: intellect, emotional state, and spiritual soul-mission.",
        "positions": [
            ("The Crown of Reason (Mind)", "What your logical intellect believes, plans, or overanalyzes."),
            ("The Well of Feeling (Heart)", "Deep emotional currents, hidden yearnings, and relational truth."),
            ("The Eternal Spark (Spirit)", "Soul evolution, karmic lesson, and higher self guidance.")
        ]
    },
    "pentagram": {
        "id": "pentagram",
        "name": "The Cross of Truth (5-Card Spread)",
        "card_count": 5,
        "description": "An intimate, penetrating spread examining the heart of a situation and its subterranean currents.",
        "positions": [
            ("The Heart of the Matter", "The core situation in its purest, unvarnished form."),
            ("The Crossing Obstacle", "What crosses you: immediate challenge, resistance, or friction."),
            ("Subterranean Roots", "Subconscious motives, past actions, or buried truths."),
            ("Guiding Crown", "Highest ideal, best potential outcome, or cosmic ally."),
            ("The Final Resolution", "The inevitable harvest if current energies continue uninterrupted.")
        ]
    },
    "celtic_cross": {
        "id": "celtic_cross",
        "name": "The Grand Celtic Cross (10-Card Spread)",
        "card_count": 10,
        "description": "The revered master spread of divination, unveiling every facet of destiny and agency.",
        "positions": [
            ("1. The Present Center", "The atmosphere surrounding the querent right now."),
            ("2. The Crossing Cross", "What challenges, opposes, or tests the center."),
            ("3. Distant Past / Foundation", "The historical events or childhood roots that formed this."),
            ("4. Subconscious / Soil", "Deep psychological drivers operating beneath awareness."),
            ("5. Crown Potential", "The highest peak possible; what can be achieved with wisdom."),
            ("6. Near Future", "The next immediate phase arriving on the horizon."),
            ("7. The Querent's Stance", "Your current self-image, attitude, and personal agency."),
            ("8. The Environment", "External forces, family, friends, enemies, and society."),
            ("9. Hopes & Secret Fears", "Your innermost unspoken desires and midnight dreads."),
            ("10. Ultimate Destination", "The grand synthesis and culmination of this life chapter.")
        ]
    },
    "horseshoe": {
        "id": "horseshoe",
        "name": "The Horseshoe of Fate (7-Card Spread)",
        "card_count": 7,
        "description": "Traces the curve of fortune from past influences to the decisive advice and outcome.",
        "positions": [
            ("1. The Past Influence", "Energies recently departed that still tint the air."),
            ("2. The Present Stance", "Where you stand in this very breath."),
            ("3. Hidden Influences", "Unseen factors or unexpected variables."),
            ("4. The Obstacle", "The barrier that must be crossed or dismantled."),
            ("5. Surrounding Energies", "The attitudes and opinions of those around you."),
            ("6. The Best Action", "The decisive course of conduct recommended by the oracle."),
            ("7. The Final Harvest", "The ultimate resolution of your journey.")
        ]
    }
}
