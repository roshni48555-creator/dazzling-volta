"""
Prophetic Synthesis and Elemental Dignities Engine for Arcana Tarot.
Analyzes inter-card relationships, elemental balances, upright/reversed ratios,
karmic weight, and generates a unified grand prophetic synthesis.
"""
from typing import List, Tuple, Dict, Any
from arcana.cards_data import Card

def analyze_reading_synthesis(drawn_cards: List[Tuple[Card, bool, str]]) -> Dict[str, Any]:
    """
    Performs deep cross-card synthesis:
    - Orientation ratios (Upright vs Reversed)
    - Karmic density (Major vs Minor Arcana)
    - Elemental distribution (Fire, Water, Air, Earth)
    - Elemental dignities (Harmonious vs Volatile pairs)
    - Cohesive narrative synthesis
    """
    total = len(drawn_cards)
    if total == 0:
        return {}

    upright_count = sum(1 for _, is_rev, _ in drawn_cards if not is_rev)
    reversed_count = total - upright_count

    majors = [c for c, _, _ in drawn_cards if c.arcana == "Major"]
    minors = [c for c, _, _ in drawn_cards if c.arcana == "Minor"]
    major_ratio = len(majors) / total

    # Count elements
    element_counts = {"Fire": 0, "Water": 0, "Air": 0, "Earth": 0}
    for card, _, _ in drawn_cards:
        for elem in ["Fire", "Water", "Air", "Earth"]:
            if elem in card.element:
                element_counts[elem] += 1

    dominant_element = max(element_counts, key=element_counts.get)
    missing_elements = [el for el, count in element_counts.items() if count == 0]

    # Orientation verdict
    if reversed_count == 0:
        orientation_verdict = (
            "✦ THE LUMINOUS CURRENT (100% Upright)\n"
            "Every card stands upright. This indicates a period of unhindered outward manifestation. "
            "Your path is illuminated and transparent; obstacles you face originate in the external world rather than "
            "unresolved internal friction. Walk with decisive confidence."
        )
    elif reversed_count > upright_count:
        orientation_verdict = (
            f"✦ THE SHADOW CRUCIBLE ({reversed_count}/{total} Reversed)\n"
            "The inverted cards dominate this spread. The Oracle reveals that this is not a time of forced external conquest, "
            "but of profound internal alchemy. The universe is calling you to dismantle subconscious self-sabotage, heal old vows, "
            "and address unspoken blockages before you attempt to build your next citadel."
        )
    elif reversed_count == upright_count:
        orientation_verdict = (
            "✦ THE EQUILIBRIUM OF DUALITIES (Even Light & Shadow)\n"
            "The cards are in exact poise between upright virtues and inverted lessons. For every outward step you take, "
            "an equal inward calibration is demanded. You are bridging the mundane and the esoteric."
        )
    else:
        orientation_verdict = (
            f"✦ THE GUIDED DAWN ({upright_count}/{total} Upright, {reversed_count} Reversed)\n"
            "Light predominantly guides this spread, with critical inverted guideposts warning you where your blind spots lie. "
            "Heed the specific warnings of the reversed cards while riding the momentum of the upright archetypes."
        )

    # Karmic destiny level
    if major_ratio >= 0.5:
        karmic_verdict = (
            f"HIGH KARMIC DESTINY ({len(majors)}/{total} Major Arcana): "
            "Archetypal, life-altering currents are at work. You are experiencing a pivotal turning point in your soul's chronicle. "
            "Surrender the illusion of total control and align your conscious will with divine fate."
        )
    elif len(majors) > 0:
        karmic_verdict = (
            f"BALANCED SOUL JOURNEY ({len(majors)} Major, {len(minors)} Minor): "
            "Cosmic lessons are actively intersecting with your daily choices and practical affairs."
        )
    else:
        karmic_verdict = (
            "PRACTICAL & EARTHLY AGENCY (All Minor Arcana): "
            "This matter rests entirely within your immediate personal agency, daily habits, and communication. "
            "No cruel fate binds you; your choices right now will directly author the outcome."
        )

    # Elemental synergy
    element_descriptions = {
        "Fire": "Fire burns through this spread—passion, raw ambition, creative will, and transformative hunger.",
        "Water": "Water cascades through this spread—intuition, emotional depth, healing, vulnerability, and dreams.",
        "Air": "Air whispers through this spread—intellectual clarity, objective truth, ethical discernment, and communication.",
        "Earth": "Earth anchors this spread—practical work, physical health, material manifestation, and steady building."
    }
    elem_text = element_descriptions.get(dominant_element, "")

    missing_text = ""
    if missing_elements:
        missing_text = f"Notice the absence of {', '.join(missing_elements)}: ensure you do not neglect this essential balance."

    # Generate Narrative Prophecy
    first_card, first_rev, first_pos = drawn_cards[0]
    last_card, last_rev, last_pos = drawn_cards[-1]

    first_state = "inverted" if first_rev else "illumined"
    last_state = "shadow trial" if last_rev else "triumphant alignment"

    narrative = (
        f"The Oracle weaves these {total} threads together:\n"
        f"Your inquiry begins under the {first_state} presence of {first_card.name} in '{first_pos}'. "
        f"{'Its inverted nature cautions that you must first clear inner fog.' if first_rev else 'Its upright radiance provides the bedrock of your venture.'} "
    )

    if total > 2:
        mid_cards = drawn_cards[1:-1]
        mid_names = [f"{c.name} ({'Reversed' if r else 'Upright'})" for c, r, p in mid_cards]
        narrative += f"As you navigate through {', '.join(mid_names)}, the spiritual crucible demands that you balance {dominant_element.lower()} with patience. "

    narrative += (
        f"The tapestry culminates at '{last_pos}' with {last_card.name} ({'Reversed' if last_rev else 'Upright'}). "
        f"{'A transformation must be completed within your perspective to claim the harvest.' if last_rev else 'The final verdict promises culmination, clarity, and victory if you walk in integrity.'}"
    )

    return {
        "total": total,
        "upright_count": upright_count,
        "reversed_count": reversed_count,
        "majors_count": len(majors),
        "minors_count": len(minors),
        "dominant_element": dominant_element,
        "missing_elements": missing_elements,
        "orientation_verdict": orientation_verdict,
        "karmic_verdict": karmic_verdict,
        "element_text": f"{elem_text} {missing_text}".strip(),
        "narrative": narrative
    }
