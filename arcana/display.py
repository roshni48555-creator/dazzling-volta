"""
Display and UI Engine for Arcana Tarot.
Powered by Rich with fallback support, smooth typewriter effect,
shuffling animations, card flip transitions, and atmospheric layouts.
"""
import sys
import time
import os
from typing import List, Dict, Tuple, Optional, Any

# Ensure UTF-8 across all streams
if sys.platform == "win32":
    os.system("")  # Enable ANSI terminal processing
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from arcana.cards_data import Card, CardMeaning
from arcana.ascii_art import (
    BANNER_LOGO, CARD_WIDTH, render_card_ascii,
    merge_cards_horizontal, get_card_back_art, get_card_turning_art
)
from arcana import sound

# Initialize global Rich console
console = Console(legacy_windows=False, highlight=False)

TYPEWRITER_SPEED = 0.012  # Seconds per char for storytelling
ANIMATION_ENABLED = True

def clear_screen():
    os.system("cls" if sys.platform == "win32" else "clear")

def set_animation(enabled: bool):
    global ANIMATION_ENABLED
    ANIMATION_ENABLED = enabled

def typewrite(text: str, style: str = "white", delay: Optional[float] = None, end: str = "\n"):
    """Prints text with an atmospheric typewriter cadence."""
    if delay is None:
        delay = TYPEWRITER_SPEED
    if not ANIMATION_ENABLED or delay <= 0:
        console.print(f"[{style}]{text}[/{style}]", end=end)
        return

    # Use rich Text with styled segments
    t = Text(style=style)
    # Output character by character or in small chunks for smoothness
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if end:
        sys.stdout.write(end)
        sys.stdout.flush()

def print_banner():
    """Prints the glowing mystical logo and title."""
    console.print(f"[bold magenta]{BANNER_LOGO}[/bold magenta]")
    console.print(
        "[bold cyan]✦ The Oracle of Sacred Geometry, Upright Wisdom & Inverted Shadows ✦[/bold cyan]",
        justify="center"
    )
    console.print("[dim italic]Enter with reverence. The cards do not predict what is fixed—they reveal what is fluid.[/dim italic]\n", justify="center")

def animate_shuffling(ritual_name: str = "The Riffle of the Seven Spheres"):
    """Plays an interactive shuffling animation with audio."""
    if not ANIMATION_ENABLED:
        console.print(f"[bold cyan]✦ Shuffling the 78 Arcanas ({ritual_name})...[/bold cyan]")
        return

    console.print(f"\n[bold magenta]🎴 Initiating {ritual_name}...[/bold magenta]")
    sound.play_shuffle()

    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold magenta"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=30, style="magenta", complete_style="bold gold1"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Gathering the scattered arcanas...", total=100)
        time.sleep(0.3)
        progress.update(task, advance=25, description="Cleansing the deck over burning frankincense...")
        time.sleep(0.35)
        progress.update(task, advance=30, description="Splitting into dual pillars of light and shadow...")
        time.sleep(0.35)
        progress.update(task, advance=25, description="Interlacing upright threads with inverted possibilities...")
        time.sleep(0.35)
        progress.update(task, advance=20, description="Harmonizing the celestial deck...")
        time.sleep(0.2)

    console.print("[bold gold1]✦ The cards are cleansed, shuffled, and resting in balance. ✦[/bold gold1]\n")

def animate_card_reveal(card: Card, is_reversed: bool, position_name: str = "") -> None:
    """Animates the dramatic reveal of a single card."""
    if position_name:
        console.print(f"\n[bold gold1]═══ {position_name.upper()} ═══[/bold gold1]")

    if not ANIMATION_ENABLED:
        sound.play_reveal() if not is_reversed else sound.play_shadow_reveal()
        _print_single_card_banner(card, is_reversed)
        return

    # Frame 1: Card back
    back_lines = get_card_back_art()
    console.print("[dim cyan]" + "\n".join(back_lines) + "[/dim cyan]")
    sound.play_card_flip()
    time.sleep(0.35)

    # Frame 2: Card turning
    # Overwrite or scroll with turning visual
    turning_lines = get_card_turning_art()
    console.print("[bold yellow]" + "\n".join(turning_lines) + "[/bold yellow]")
    time.sleep(0.35)

    # Frame 3: Final Card Reveal
    if is_reversed:
        sound.play_shadow_reveal()
    else:
        sound.play_reveal()

    _print_single_card_banner(card, is_reversed)

def _print_single_card_banner(card: Card, is_reversed: bool):
    """Prints the ASCII card with rich colors."""
    ascii_lines = render_card_ascii(card, is_reversed)
    color = "bold red" if is_reversed else "bold gold1"
    banner_text = f"✦ REVEALED: {card.name.upper()} ({'REVERSED' if is_reversed else 'UPRIGHT'}) ✦"
    console.print(f"[{color}]{banner_text}[/{color}]")

    card_art = "\n".join(ascii_lines)
    style_tag = "bold red" if is_reversed else "bold cyan"
    console.print(f"[{style_tag}]{card_art}[/{style_tag}]\n")

def display_spread_cards_side_by_side(cards_drawn: List[Tuple[Card, bool, str]]):
    """
    Renders multiple drawn cards horizontally with position banners.
    cards_drawn is a list of tuples: (card, is_reversed, position_name)
    """
    # Print in chunks of 3 cards per row for optimal terminal fit
    chunk_size = 3
    for i in range(0, len(cards_drawn), chunk_size):
        chunk = cards_drawn[i:i + chunk_size]

        # Top headers (position names)
        header_parts = []
        for card, is_rev, pos in chunk:
            rev_label = "▼ REV" if is_rev else "▲ UPR"
            hdr = f"{pos[:18]} ({rev_label})"
            header_parts.append(hdr.center(CARD_WIDTH))
        console.print("[bold gold1]" + "  ".join(header_parts) + "[/bold gold1]")

        # ASCII arts
        arts = [render_card_ascii(c, is_rev) for c, is_rev, pos in chunk]
        merged = merge_cards_horizontal(arts, spacing=2)

        # Style according to predominant orientation in chunk
        console.print(f"[cyan]{merged}[/cyan]\n")

def display_card_full_reading(card: Card, is_reversed: bool, position_name: str = "", position_role: str = ""):
    """Displays the comprehensive reading and prophecy breakdown for a card."""
    meaning: CardMeaning = card.reversed if is_reversed else card.upright
    status_label = "REVERSED [Inverted Mirror / Shadow]" if is_reversed else "UPRIGHT [Direct Virtue / Manifestation]"
    theme_color = "red" if is_reversed else "cyan"

    title_text = f"{card.numeral} · {card.name} ({status_label})"
    if position_name:
        title_text = f"[{position_name.upper()}] — {title_text}"

    # Build Content Table
    content = Text()
    content.append(f"✦ Archetype: ", style="bold gold1")
    content.append(f"{meaning.archetype}\n", style="italic white")

    content.append(f"✦ Essence: ", style="bold gold1")
    content.append(f"{card.essence}\n", style="white")

    content.append(f"✦ Keywords: ", style="bold gold1")
    content.append(f"{', '.join(meaning.keywords)}\n", style="bold yellow")

    content.append(f"✦ Elemental Aspect: ", style="bold gold1")
    content.append(f"{card.element} ({card.sigil}) | Planetary/Astrological: {card.zodiac_planet}\n\n", style="cyan")

    content.append("─── PROPHECY & DEEP INTERPRETATION ───\n", style="bold magenta")
    content.append(f"{meaning.prophecy}\n\n", style="bright_white")

    content.append("─── THE THREE MIRRORS ───\n", style="bold magenta")
    content.append("❤️  Heart & Bonds: ", style="bold red")
    content.append(f"{meaning.love}\n", style="white")
    content.append("💼 Path & Ambition: ", style="bold green")
    content.append(f"{meaning.career}\n", style="white")
    content.append("👁️  Soul & Shadow: ", style="bold blue")
    content.append(f"{meaning.spiritual}\n\n", style="white")

    action_label = "⚠️  CAUTIONARY WARNING: " if is_reversed else "⚡ ORACLE'S DIRECT ADVICE: "
    content.append(action_label, style="bold red" if is_reversed else "bold yellow")
    content.append(f"{meaning.advice}\n", style="bold bright_white")

    panel = Panel(
        content,
        title=f"[bold {theme_color}]✦ {title_text} ✦[/bold {theme_color}]",
        subtitle=f"[dim]{position_role}[/dim]" if position_role else None,
        border_style=theme_color,
        padding=(1, 2)
    )
    console.print(panel)
    console.print()

def ask_choice(prompt_text: str, options: List[str], default: int = 1) -> int:
    """Presents a styled list of choices and returns the 1-based index."""
    console.print(f"\n[bold gold1]{prompt_text}[/bold gold1]")
    for idx, opt in enumerate(options, start=1):
        console.print(f"  [bold cyan][{idx}][/bold cyan] {opt}")
    
    valid_range = [str(i) for i in range(1, len(options) + 1)]
    while True:
        choice = Prompt.ask(
            f"[bold magenta]Select your path (1-{len(options)})[/bold magenta]",
            default=str(default)
        )
        if choice in valid_range:
            return int(choice)
        console.print(f"[red]Please enter a number between 1 and {len(options)}.[/red]")

def press_to_continue(message: str = "Press Enter to consult the Veil..."):
    """Pauses until user presses Enter."""
    console.print(f"\n[dim italic]{message}[/dim italic]", end="")
    try:
        input()
    except EOFError:
        pass
