"""
Comprehensive flow validation test for Arcana Tarot.
Tests each module's core functions end-to-end to ensure zero runtime issues.
"""
import sys
import os

if sys.platform == "win32":
    os.system("")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

from arcana.cards_data import ALL_CARDS, MAJOR_ARCANA, MINOR_ARCANA, CARD_LOOKUP
from arcana.engine import TarotDeck, SPREAD_DEFINITIONS, DeckOrientationSetting
from arcana.synthesis import analyze_reading_synthesis
from arcana.ascii_art import (
    render_card_ascii, merge_cards_horizontal, get_card_back_art,
    get_card_turning_art, get_spread_map_celtic_cross
)
from arcana.game_duel import calculate_card_combat_effect, DuelFighter
from arcana.celestial import ZODIAC_CORRESPONDENCES
from arcana.grimoire import save_reading_to_journal, CHRONICLE_FILE
from arcana import sound

def test_deck_and_cards():
    assert len(ALL_CARDS) == 78, f"Expected 78 cards, got {len(ALL_CARDS)}"
    assert len(MAJOR_ARCANA) == 22, f"Expected 22 major, got {len(MAJOR_ARCANA)}"
    assert len(MINOR_ARCANA) == 56, f"Expected 56 minor, got {len(MINOR_ARCANA)}"

    deck = TarotDeck(DeckOrientationSetting.BALANCED)
    deck.shuffle_riffle()
    deck.cut_deck(0.33)
    c1, r1 = deck.draw_top()
    c2, r2 = deck.draw_top()
    assert c1 is not None and isinstance(r1, bool)
    assert c2 is not None and isinstance(r2, bool)
    print("✓ Deck & draw mechanics: PASS")

def test_ascii_art():
    for card in MAJOR_ARCANA[:3]:
        up_lines = render_card_ascii(card, False)
        rev_lines = render_card_ascii(card, True)
        assert len(up_lines) == 12, f"Card height expected 12, got {len(up_lines)}"
        assert len(rev_lines) == 12
        merged = merge_cards_horizontal([up_lines, rev_lines])
        assert len(merged) > 0

    assert len(get_card_back_art()) > 0
    assert len(get_card_turning_art()) > 0
    assert len(get_spread_map_celtic_cross()) > 0
    print("✓ ASCII Art & Card rendering: PASS")

def test_synthesis():
    deck = TarotDeck()
    deck.shuffle_riffle()
    drawn = []
    for pos_title, pos_desc in SPREAD_DEFINITIONS["celtic_cross"]["positions"]:
        c, r = deck.draw_top()
        drawn.append((c, r, pos_title))

    synth = analyze_reading_synthesis(drawn)
    assert "narrative" in synth
    assert "orientation_verdict" in synth
    assert "karmic_verdict" in synth
    assert "dominant_element" in synth
    print(f"✓ Celtic Cross 10-Card Synthesis: PASS ({synth['dominant_element']}, {synth['upright_count']} Upr / {synth['reversed_count']} Rev)")

def test_duel_mechanics():
    p = DuelFighter("Hero")
    s = DuelFighter("Shadow", is_ai=True)
    p.gain_shield(20)
    p.take_damage(15)
    assert p.shield == 5 and p.hp == 100
    p.take_damage(10)
    assert p.shield == 0 and p.hp == 95

    # Check various combat card effects
    for card in MAJOR_ARCANA:
        eff_up = calculate_card_combat_effect(card, False)
        eff_rev = calculate_card_combat_effect(card, True)
        assert eff_up[1] >= 0 or eff_up[2] >= 0
        assert eff_rev[1] >= 0 or eff_rev[2] >= 0
    print("✓ Duel combat engine: PASS")

def test_grimoire_journal():
    dummy_drawn = [
        (MAJOR_ARCANA[0], False, "Roots"),
        (MAJOR_ARCANA[1], True, "Crown")
    ]
    dummy_synth = {"narrative": "Test destiny", "orientation_verdict": "Test balance"}
    save_reading_to_journal("Test Spread", "Test Inquiry", dummy_drawn, dummy_synth)
    assert os.path.exists(CHRONICLE_FILE)
    print("✓ Grimoire persistence: PASS")

if __name__ == "__main__":
    print("Running Arcana Test Suite...")
    test_deck_and_cards()
    test_ascii_art()
    test_synthesis()
    test_duel_mechanics()
    test_grimoire_journal()
    print("\n🎉 ALL 5 TEST SUITES PASSED FLAWLESSLY! 🎉")
