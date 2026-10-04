"""
Celestial Alignment and Daily Oracle Engine for Arcana Tarot.
Calculates astrological correspondences, zodiac rulers,
and generates the personalized Daily Tarot Oracle.
"""
from datetime import date
from typing import Dict, Tuple
from rich.panel import Panel

from arcana.display import console, ask_choice, press_to_continue, animate_card_reveal, display_card_full_reading
from arcana.cards_data import MAJOR_ARCANA, ALL_CARDS, Card
from arcana.engine import TarotDeck
from arcana import sound

ZODIAC_CORRESPONDENCES = {
    "Aries": ("The Emperor", "Mars", "Fire", "March 21 - April 19", "I Am · Sovereign Will"),
    "Taurus": ("The Hierophant", "Venus", "Earth", "April 20 - May 20", "I Have · Sacred Tradition"),
    "Gemini": ("The Lovers", "Mercury", "Air", "May 21 - June 20", "I Think · Sacred Choice"),
    "Cancer": ("The Chariot", "Moon", "Water", "June 21 - July 22", "I Feel · Victorious Will"),
    "Leo": ("Strength", "Sun", "Fire", "July 23 - August 22", "I Will · Quiet Courage"),
    "Virgo": ("The Hermit", "Mercury", "Earth", "August 23 - September 22", "I Analyze · Inner Light"),
    "Libra": ("Justice", "Venus", "Air", "September 23 - October 22", "I Balance · Absolute Truth"),
    "Scorpio": ("Death", "Pluto / Mars", "Water", "October 23 - November 21", "I Transform · Sacred Rebirth"),
    "Sagittarius": ("Temperance", "Jupiter", "Fire", "November 22 - December 21", "I See · Divine Equilibrium"),
    "Capricorn": ("The Devil", "Saturn", "Earth", "December 22 - January 19", "I Use · Unmasking Illusion"),
    "Aquarius": ("The Star", "Uranus / Saturn", "Air", "January 20 - February 18", "I Know · Celestial Hope"),
    "Pisces": ("The Moon", "Neptune / Jupiter", "Water", "February 19 - March 20", "I Believe · Piercing the Veil")
}

def run_celestial_alignment():
    """Runs the interactive Daily Oracle and Zodiac Alignment."""
    console.clear()
    sound.play_omen_bell()
    console.print("[bold gold1]═══════════ THE CELESTIAL HOROSCOPE & DAILY ORACLE ═══════════[/bold gold1]\n")
    console.print("Align your spirit with the celestial spheres and draw your personal card of the day.\n")

    zodiac_keys = list(ZODIAC_CORRESPONDENCES.keys())
    options = [f"{sign} ({ZODIAC_CORRESPONDENCES[sign][3]})" for sign in zodiac_keys]
    options.append("Skip Zodiac Selection (Pure Celestial Randomness)")

    choice = ask_choice("Select your Zodiac Sun Sign:", options)

    selected_sign = None
    if choice <= len(zodiac_keys):
        selected_sign = zodiac_keys[choice - 1]
        tarot_archetype, planet, element, dates, mantra = ZODIAC_CORRESPONDENCES[selected_sign]

        info_panel = (
            f"[bold gold1]✦ ZODIAC SUN SIGN: {selected_sign.upper()} ✦[/bold gold1]\n"
            f"• Planetary Ruler: [bold cyan]{planet}[/bold cyan] | Element: [bold red]{element}[/bold red]\n"
            f"• Archetypal Major Arcana: [bold magenta]{tarot_archetype}[/bold magenta]\n"
            f"• Soul Mantra: [italic white]'{mantra}'[/italic white]"
        )
        console.print(Panel(info_panel, border_style="gold1"))

    today_str = date.today().strftime("%B %d, %Y")
    console.print(f"\n[bold cyan]Drawing your Daily Oracle for {today_str}...[/bold cyan]")
    press_to_continue("Press Enter to draw your Card of the Day...")

    # Draw card
    deck = TarotDeck()
    deck.shuffle_riffle()
    card, is_rev = deck.draw_top()

    animate_card_reveal(card, is_rev, f"DAILY ORACLE FOR {today_str.upper()}")
    display_card_full_reading(card, is_rev, f"DAILY CARD: {card.name}")

    meaning = card.reversed if is_rev else card.upright
    mantra_text = (
        f"[bold gold1]✦ TODAY'S SACRED MANTRA ✦[/bold gold1]\n\n"
        f"[bright_white]\"Through the presence of {card.name} ({'Reversed' if is_rev else 'Upright'}), "
        f"I open my eyes to {meaning.keywords[0].lower()} and walk with unwavering integrity.\"[/bright_white]"
    )
    console.print(Panel(mantra_text, border_style="gold1", padding=(1, 2)))
    press_to_continue()
