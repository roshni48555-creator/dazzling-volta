"""
The Divination Sanctuary for Arcana Tarot.
Executes authentic multi-card Tarot spreads with interactive rituals,
custom deck cuts, card-by-card reveals, side-by-side terminal layouts,
deep positional interpretations, and grand holistic synthesis.
"""
from typing import List, Tuple, Dict, Any
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from arcana.display import (
    console, typewrite, animate_shuffling, animate_card_reveal,
    display_spread_cards_side_by_side, display_card_full_reading,
    ask_choice, press_to_continue
)
from arcana.engine import TarotDeck, SPREAD_DEFINITIONS
from arcana.ascii_art import (
    get_spread_map_celtic_cross, get_spread_map_trinity, get_spread_map_pentagram
)
from arcana.synthesis import analyze_reading_synthesis
from arcana.grimoire import save_reading_to_journal
from arcana import sound

def run_divination_sanctuary(deck: TarotDeck):
    """Main entry point for authentic Tarot spreads and readings."""
    while True:
        console.clear()
        sound.play_omen_bell()
        console.print("[bold gold1]═══════════ THE DIVINATION SANCTUARY OF THE SPHINX ═══════════[/bold gold1]\n")
        console.print("Choose an authentic sacred spread to lay upon the velvet altar.\n")

        spread_keys = list(SPREAD_DEFINITIONS.keys())
        options = [
            f"{SPREAD_DEFINITIONS[k]['name']} — {SPREAD_DEFINITIONS[k]['description']}"
            for k in spread_keys
        ]
        options.append("Return to Main Menu")

        choice = ask_choice("Select your Divination Spread:", options)
        if choice > len(spread_keys):
            break

        selected_key = spread_keys[choice - 1]
        spread_info = SPREAD_DEFINITIONS[selected_key]
        _perform_spread_reading(deck, spread_info)

def _perform_spread_reading(deck: TarotDeck, spread_info: Dict[str, Any]):
    console.clear()
    spread_name = spread_info["name"]
    card_count = spread_info["card_count"]
    positions = spread_info["positions"]

    console.print(f"[bold gold1]✦ THE SANCTUARY: {spread_name.upper()} ✦[/bold gold1]\n")
    console.print(f"[dim italic]{spread_info['description']}[/dim italic]\n")

    # Step 1: Intention / Inquiry
    console.print("[bold cyan]✦ STEP 1: SETTING YOUR SACRED INTENTION ✦[/bold cyan]")
    inquiry_preset = ask_choice(
        "Choose the focus domain of your inquiry:",
        [
            "General Life Path & Spiritual Compass",
            "Matters of the Heart, Love & Soul Connections",
            "Vocation, Creative Ambition & Prosperity",
            "Shadow Work, Subconscious Blocks & Hidden Truth",
            "Custom Specific Question (Type your own)"
        ]
    )

    inquiry_text = ""
    if inquiry_preset == 5:
        inquiry_text = Prompt.ask("[bold magenta]Inscribe your specific inquiry for the Oracle[/bold magenta]")
    else:
        preset_names = [
            "General Life Path & Spiritual Compass",
            "Matters of the Heart, Love & Soul Connections",
            "Vocation, Creative Ambition & Prosperity",
            "Shadow Work, Subconscious Blocks & Hidden Truth"
        ]
        inquiry_text = preset_names[inquiry_preset - 1]

    # Step 2: Shuffling Ritual
    console.clear()
    console.print("[bold cyan]✦ STEP 2: THE SHUFFLE RITUAL ✦[/bold cyan]")
    deck.reset_deck()
    deck.shuffle_riffle()
    animate_shuffling()

    # Step 3: Cutting the Deck
    console.print("[bold cyan]✦ STEP 3: CUTTING THE DECK ✦[/bold cyan]")
    cut_choice = ask_choice(
        "Where will your hands divide the deck?",
        [
            "Shallow Cut (Upper 25% — Fast, fiery celestial energy)",
            "Center Cut (Middle 50% — Balanced, grounded alignment)",
            "Deep Abyssal Cut (Lower 75% — Subterranean, ancestral roots)",
            "The Weaver's Hand (Intuitive random split)"
        ]
    )
    cut_fractions = [0.25, 0.50, 0.75, 0.42]
    deck.cut_deck(cut_fractions[cut_choice - 1])
    console.print("[bold green]✦ The deck has been cut and rejoined. Destiny is primed. ✦[/bold green]\n")
    press_to_continue("Press Enter to draw the arcanas...")

    # Step 4: The Draw & Reveal
    console.clear()
    console.print(f"[bold gold1]═══════════ THE SACRED REVEAL: {spread_name.upper()} ═══════════[/bold gold1]\n")
    console.print(f"[dim]Inquiry: '{inquiry_text}'[/dim]\n")

    # Display Spread Map if available
    if spread_info["id"] == "celtic_cross":
        console.print(f"[dim cyan]{get_spread_map_celtic_cross()}[/dim cyan]\n")
    elif spread_info["id"] == "trinity":
        console.print(f"[dim cyan]{get_spread_map_trinity()}[/dim cyan]\n")
    elif spread_info["id"] == "pentagram":
        console.print(f"[dim cyan]{get_spread_map_pentagram()}[/dim cyan]\n")

    drawn_cards: List[Tuple[Any, bool, str]] = []

    for idx in range(card_count):
        pos_title, pos_desc = positions[idx]
        card, is_rev = deck.draw_top()
        drawn_cards.append((card, is_rev, pos_title))

        console.print(f"[bold gold1]═══ DRAWING CARD {idx + 1}/{card_count}: {pos_title} ═══[/bold gold1]")
        console.print(f"[dim italic]Role: {pos_desc}[/dim italic]")
        animate_card_reveal(card, is_rev, pos_title)
        press_to_continue("Press Enter to continue...")

    # Step 5: Master Altar Spread (Side-by-side cards)
    console.clear()
    console.print(f"[bold gold1]═══════════════ THE ALTAR OF {spread_name.upper()} ═══════════════[/bold gold1]\n")
    console.print(f"[bold cyan]INQUIRY: \"{inquiry_text}\"[/bold cyan]\n")
    display_spread_cards_side_by_side(drawn_cards)
    press_to_continue("Press Enter to begin the deep position-by-position prophecy...")

    # Step 6: Detailed Interpretations
    console.clear()
    console.print("[bold gold1]═══════════ POSITION-BY-POSITION PROPHECY ═══════════[/bold gold1]\n")
    for idx, (card, is_rev, pos_title) in enumerate(drawn_cards):
        pos_desc = positions[idx][1]
        display_card_full_reading(card, is_rev, pos_title, pos_desc)

    press_to_continue("Press Enter to receive the Grand Prophetic Synthesis...")

    # Step 7: Grand Synthesis
    console.clear()
    console.print("[bold gold1]═══════════ THE ORACLE'S GRAND SYNTHESIS ═══════════[/bold gold1]\n")
    synthesis = analyze_reading_synthesis(drawn_cards)

    console.print(Panel(
        f"[bold gold1]{synthesis['orientation_verdict']}[/bold gold1]\n\n"
        f"[bold cyan]✦ KARMIC PROFILE:[/bold cyan] {synthesis['karmic_verdict']}\n"
        f"[bold magenta]✦ ELEMENTAL DYNAMICS:[/bold magenta] {synthesis['element_text']}\n\n"
        f"[bold white]✦ THE TAPESTRY OF DESTINY:[/bold white]\n"
        f"[italic bright_white]{synthesis['narrative']}[/italic bright_white]",
        title=f"[bold gold1]✦ MASTER SYNTHESIS: {spread_name.upper()} ✦[/bold gold1]",
        border_style="gold1",
        padding=(1, 2)
    ))

    # Auto-save to Journal
    save_reading_to_journal(spread_name, inquiry_text, drawn_cards, synthesis)
    console.print("\n[dim green]✔ This prophecy has been automatically inscribed into your sacred journal chronicle.[/dim green]")

    press_to_continue("Press Enter to return to the Sanctuary Menu...")
