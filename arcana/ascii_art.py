"""
ASCII Art and Visual Card Layout Engine for Arcana Tarot.
Renders intricate card frames, upright/reversed orientations,
shuffling animations, spread maps, and side-by-side terminal layouts.
"""
from typing import List, Dict, Tuple, Optional
from arcana.cards_data import Card

# Standard card dimensions
CARD_WIDTH = 26
CARD_HEIGHT = 14

BANNER_LOGO = r"""
  █████╗ ██████╗  ██████╗ █████╗ ███╗   ██╗ █████╗ 
 ██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔══██╗
 ███████║██████╔╝██║     ███████║██╔██╗ ██║███████║
 ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗██║██╔══██║
 ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████║██║  ██║
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
     ───✦  V E I L   O F   D E S T I N Y  ✦───
"""

# Unique miniature ASCII emblems for Major Arcana (5x4)
MAJOR_ICONS = {
    "maj_00": [  # The Fool
        r"   \o/   ",
        r"    |    ",
        r"   / \   ",
        r"  ~~~/~  "
    ],
    "maj_01": [  # The Magician
        r"   /\   ",
        r"  ( \/ ) ",
        r"   \  /  ",
        r"  --██-- "
    ],
    "maj_02": [  # High Priestess
        r"   _O_   ",
        r"  ( B )  ",
        r"  | J |  ",
        r"  =====  "
    ],
    "maj_03": [  # The Empress
        r"  \*** / ",
        r"   (o)   ",
        r"  / * \  ",
        r"  ~✿~✿~  "
    ],
    "maj_04": [  # The Emperor
        r"  [WWWWW]",
        r"   |#|   ",
        r"  /###\  ",
        r" [=======]"
    ],
    "maj_05": [  # The Hierophant
        r"   _☩_   ",
        r"  -=☩=-  ",
        r"   |☩|   ",
        r"  /   \  "
    ],
    "maj_06": [  # The Lovers
        r"  <3  <3 ",
        r" (o)  (o)",
        r"  \ \/ / ",
        r"   \__/  "
    ],
    "maj_07": [  # The Chariot
        r"   / \   ",
        r"  [===]  ",
        r"  (o)(o) ",
        r"  ~===~  "
    ],
    "maj_08": [  # Strength
        r"  ( oo ) ",
        r" / \/ \  ",
        r" \_/\_/  ",
        r"  ~♌~♌~  "
    ],
    "maj_09": [  # The Hermit
        r"    *    ",
        r"   /|\   ",
        r"  ( | )  ",
        r"   / \   "
    ],
    "maj_10": [  # Wheel of Fortune
        r"   _O_   ",
        r"  / | \  ",
        r" | -O- | ",
        r"  \ | /  "
    ],
    "maj_11": [  # Justice
        r"   _^_   ",
        r"  (===)  ",
        r"  / | \  ",
        r" 0  |  0 "
    ],
    "maj_12": [  # The Hanged Man
        r"  \___/  ",
        r"   | |   ",
        r"  / * \  ",
        r"   \O/   "
    ],
    "maj_13": [  # Death
        r"   ,-.   ",
        r"  (o.o)  ",
        r"   |=/   ",
        r"  / / \  "
    ],
    "maj_14": [  # Temperance
        r"  \ | /  ",
        r"   (_)   ",
        r"  /   \  ",
        r" (==v==) "
    ],
    "maj_15": [  # The Devil
        r"  \m/ \m/",
        r"   (o.o) ",
        r"   / v \ ",
        r"  -={*}=-"
    ],
    "maj_16": [  # The Tower
        r"   / \/  ",
        r"  / / \  ",
        r" | /|  | ",
        r" ||*|  | "
    ],
    "maj_17": [  # The Star
        r"   \ /   ",
        r"  --*--  ",
        r"   / \   ",
        r"  ~ ~ ~  "
    ],
    "maj_18": [  # The Moon
        r"   .--.  ",
        r"  /   /  ",
        r"  \   \  ",
        r"   '--'  "
    ],
    "maj_19": [  # The Sun
        r"  \ | /  ",
        r" --(☼)-- ",
        r"  / | \  ",
        r"  ^^^^^  "
    ],
    "maj_20": [  # Judgement
        r"   \ /   ",
        r"  ==O==  ",
        r"   / \   ",
        r"  |/ \|  "
    ],
    "maj_21": [  # The World
        r"  .---.  ",
        r" /  O  \ ",
        r" | /|\ | ",
        r"  '---'  "
    ],
}

# Emblems for Minor Arcana suits
SUIT_ICONS = {
    "Wands": [
        r"   (^)   ",
        r"   /|\   ",
        r"   /|\   ",
        r"  (===)  "
    ],
    "Cups": [
        r"  \~~~ / ",
        r"   \_/   ",
        r"    |    ",
        r"  (===)  "
    ],
    "Swords": [
        r"    ^    ",
        r"    |    ",
        r"  --+--  ",
        r"    |    "
    ],
    "Pentacles": [
        r"   .-.   ",
        r"  ( * )  ",
        r"  ( * )  ",
        r"   '-'   "
    ],
}

def invert_icon(icon_lines: List[str]) -> List[str]:
    """Invert icon vertically and mirror characters for reversed cards."""
    inverted = []
    # Flip order of lines
    for line in reversed(icon_lines):
        # Swap directional characters
        trans = str.maketrans({
            '^': 'v', 'v': '^',
            '/': '\\', '\\': '/',
            '|': '|', '(': ')', ')': '(',
            '[': ']', ']': '[',
            '{': '}', '}': '{',
            'm': 'w', 'W': 'M', 'w': 'm'
        })
        inverted.append(line.translate(trans))
    return inverted

def get_card_back_art() -> List[str]:
    """Returns lines for a face-down Tarot card back."""
    return [
        "╔════════════════════════╗",
        "║ ░░░░░░░░░░░░░░░░░░░░░░ ║",
        "║ ░ ┌──────────────────┐ ░ ║",
        "║ ░ │  ✦   · ☽ ☼ ☾ ·   │ ░ ║",
        "║ ░ │   ╲    🜂   🜄   ╱ │ ░ ║",
        "║ ░ │    ╲    👁    ╱  │ ░ ║",
        "║ ░ │    ╱    ⛦    ╲  │ ░ ║",
        "║ ░ │   ╱    🜃   🜁   ╲ │ ░ ║",
        "║ ░ │  ✦   · ☽ ☼ ☾ ·   │ ░ ║",
        "║ ░ └──────────────────┘ ░ ║",
        "║ ░░░░░░░░░░░░░░░░░░░░░░ ║",
        "╚════════════════════════╝",
    ]

def get_card_turning_art() -> List[str]:
    """Returns lines for an in-transit flipping card."""
    return [
        "      ┌────────────┐      ",
        "      │ ░░░░░░░░░░ │      ",
        "      │ ░ ✦    ✦ ░ │      ",
        "      │    FLIP    │      ",
        "      │   ══►◄══   │      ",
        "      │  TURNING   │      ",
        "      │    FATE    │      ",
        "      │ ░ ✦    ✦ ░ │      ",
        "      │ ░░░░░░░░░░ │      ",
        "      └────────────┘      ",
        "                          ",
        "                          ",
    ]

def render_card_ascii(card: Card, is_reversed: bool = False) -> List[str]:
    """
    Renders a single 26-character-wide card in ASCII.
    Distinguishes Upright vs Reversed visually.
    """
    w = 26
    inner_w = w - 2  # 24

    # Top border
    if not is_reversed:
        top_border = "╔" + "═" * inner_w + "╗"
        bot_border = "╚" + "═" * inner_w + "╝"
        banner = "[▲ UPRIGHT ▲]"
    else:
        top_border = "╒" + "═" * inner_w + "╕"
        bot_border = "╘" + "═" * inner_w + "╛"
        banner = "[▼ REVERSED ▼]"

    # Card numeral / rank + name line
    header = f"{card.numeral} {card.name}"
    if len(header) > inner_w:
        header = header[:inner_w]
    header_line = f"║{header.center(inner_w)}║"

    # Status banner line
    status_line = f"║{banner.center(inner_w)}║"

    divider = f"║{'·' * inner_w}║"

    # Icon lines
    if card.id in MAJOR_ICONS:
        icon_raw = MAJOR_ICONS[card.id]
    elif card.suit and card.suit in SUIT_ICONS:
        icon_raw = SUIT_ICONS[card.suit]
    else:
        icon_raw = ["  ✦ ✦  ", "  (☼)  ", "  ✦ ✦  ", " ~~~~~ "]

    if is_reversed:
        icon_lines = invert_icon(icon_raw)
    else:
        icon_lines = icon_raw

    # Render 4 lines of icon
    art_lines = []
    for line in icon_lines:
        art_lines.append(f"║{line.center(inner_w)}║")

    # Essence / Archetype line
    meaning = card.reversed if is_reversed else card.upright
    kw_str = " · ".join(meaning.keywords[:2])
    if len(kw_str) > inner_w - 2:
        kw_str = kw_str[:inner_w - 2]
    kw_line = f"║ {kw_str.center(inner_w - 2)} ║"

    # Element and Sigil line
    elem_str = f"{card.element} {card.sigil}"
    if len(elem_str) > inner_w - 2:
        elem_str = elem_str[:inner_w - 2]
    elem_line = f"║ {elem_str.center(inner_w - 2)} ║"

    lines = [
        top_border,
        header_line,
        status_line,
        divider,
        *art_lines,
        divider,
        kw_line,
        elem_line,
        bot_border
    ]
    return lines

def merge_cards_horizontal(cards_art: List[List[str]], spacing: int = 2) -> str:
    """Combines multiple ASCII cards side-by-side into a single block."""
    if not cards_art:
        return ""
    max_lines = max(len(art) for art in cards_art)
    spacer = " " * spacing
    merged_lines = []
    for line_idx in range(max_lines):
        line_parts = []
        for art in cards_art:
            if line_idx < len(art):
                line_parts.append(art[line_idx])
            else:
                line_parts.append(" " * (len(art[0]) if art else 26))
        merged_lines.append(spacer.join(line_parts))
    return "\n".join(merged_lines)

def get_spread_map_celtic_cross() -> str:
    """ASCII map illustrating the traditional 10-card Celtic Cross spread positions."""
    return """
      ┌────────────────────────────────────────────────────────┐
      │            THE SACRED CELTIC CROSS SANCTUARY           │
      │                                                        │
      │                  [ 5. Crown Potential ]     [ 10. Outcome ]
      │                            │                           │
      │   [ 3. Distant Past ] - [1 & 2 Center] - [6. Near Future]│
      │                            │                           │
      │                  [ 4. Subconscious ]        [ 9. Hopes/Fears ]
      │                                                        │
      │                                             [ 8. Environment ]
      │                                                        │
      │                                             [ 7. Querent ]
      └────────────────────────────────────────────────────────┘
    """

def get_spread_map_trinity() -> str:
    """ASCII map illustrating the 3-card spread."""
    return """
    ┌─────────────────────────── TRINITY SPREAD ───────────────────────────┐
    │     [ CARD 1: THE ROOTS ]   [ CARD 2: THE CRUCIBLE ]   [ CARD 3: THE DAWN ]   │
    │        (Past / Origin)        (Present / Crucible)      (Future / Horizon)    │
    └───────────────────────────────────────────────────────────────────────┘
    """

def get_spread_map_pentagram() -> str:
    """ASCII map illustrating the 5-card Cross of Truth spread."""
    return """
    ┌─────────────────────────── CROSS OF TRUTH ───────────────────────────┐
    │                       [ 4. Guiding Light ]                            │
    │       [ 2. Crossing Obstacle ] ── [ 1. The Present ] ── [ 5. Destiny ]│
    │                       [ 3. Deep Roots ]                               │
    └───────────────────────────────────────────────────────────────────────┘
    """
