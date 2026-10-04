"""
The Grimoire, Journal, and Encyclopedia Codex for Arcana Tarot.
Enables browsing the complete 78-card codex, searching card lore,
saving reading histories to JSON, and exporting divination chronicles to Markdown.
"""
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from arcana.display import console, ask_choice, press_to_continue, display_card_full_reading
from arcana.cards_data import ALL_CARDS, MAJOR_ARCANA, MINOR_ARCANA, CARD_LOOKUP, NAME_LOOKUP, Card
from arcana.ascii_art import render_card_ascii

CHRONICLE_FILE = "readings_chronicle.json"

def save_reading_to_journal(spread_name: str, inquiry: str, drawn_cards: List[Any], synthesis_summary: Dict[str, Any]):
    """Saves a completed divination reading to the persistent chronicle JSON file."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "date_str": datetime.now().strftime("%B %d, %Y - %H:%M"),
        "spread_name": spread_name,
        "inquiry": inquiry or "General Spiritual Reflection",
        "cards": [
            {
                "card_id": c.id,
                "card_name": c.name,
                "is_reversed": is_rev,
                "position": pos,
                "keywords": (c.reversed if is_rev else c.upright).keywords
            }
            for c, is_rev, pos in drawn_cards
        ],
        "synthesis": synthesis_summary.get("narrative", ""),
        "orientation_verdict": synthesis_summary.get("orientation_verdict", "")
    }

    history = []
    if os.path.exists(CHRONICLE_FILE):
        try:
            with open(CHRONICLE_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(record)
    try:
        with open(CHRONICLE_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        console.print(f"[red]Failed to save to journal: {e}[/red]")

def view_reading_history():
    """Displays saved divination readings."""
    console.clear()
    console.print("[bold gold1]═══════════ THE CHRONICLE OF PAST PROPHECIES ═══════════[/bold gold1]\n")
    if not os.path.exists(CHRONICLE_FILE):
        console.print("[dim italic]Your chronicle is currently blank. Complete a divination reading to inscribe it here.[/dim italic]")
        press_to_continue()
        return

    try:
        with open(CHRONICLE_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

    if not history:
        console.print("[dim italic]Your chronicle is currently empty.[/dim italic]")
        press_to_continue()
        return

    table = Table(title="✦ RECORDED DIVINATIONS ✦", title_style="bold magenta", expand=True)
    table.add_column("No.", style="bold cyan", width=5)
    table.add_column("Date", style="bold white", width=22)
    table.add_column("Spread", style="bold yellow", width=28)
    table.add_column("Inquiry Focus", style="italic white")
    table.add_column("Cards", style="bold green", width=12)

    for idx, rec in enumerate(reversed(history[-15:]), start=1):
        real_idx = len(history) - idx + 1
        table.add_row(
            str(real_idx),
            rec.get("date_str", "Unknown"),
            rec.get("spread_name", "Spread"),
            rec.get("inquiry", "General")[:35],
            f"{len(rec.get('cards', []))} cards"
        )
    console.print(table)

    choice = ask_choice(
        "Chronicle Actions:",
        [
            "Inspect a specific reading in detail",
            "Export a reading to a formatted Markdown (.md) file",
            "Return to Main Menu"
        ]
    )

    if choice == 1:
        entry_num = Prompt.ask(f"[bold cyan]Enter reading number to view (1-{len(history)})[/bold cyan]")
        try:
            num = int(entry_num)
            if 1 <= num <= len(history):
                rec = history[num - 1]
                _render_full_record(rec)
        except ValueError:
            pass
    elif choice == 2:
        entry_num = Prompt.ask(f"[bold cyan]Enter reading number to export (1-{len(history)})[/bold cyan]")
        try:
            num = int(entry_num)
            if 1 <= num <= len(history):
                rec = history[num - 1]
                _export_record_to_markdown(rec)
        except ValueError:
            pass

def _render_full_record(rec: Dict[str, Any]):
    console.clear()
    console.print(f"[bold gold1]✦ READING #{rec.get('timestamp', '')[:10]} — {rec.get('spread_name')} ✦[/bold gold1]")
    console.print(f"[dim]Date: {rec.get('date_str')}[/dim]")
    console.print(f"[bold cyan]Inquiry: {rec.get('inquiry')}[/bold cyan]\n")

    for card_data in rec.get("cards", []):
        c_id = card_data["card_id"]
        is_rev = card_data["is_reversed"]
        pos = card_data["position"]
        c = CARD_LOOKUP.get(c_id)
        if c:
            display_card_full_reading(c, is_rev, pos)

    console.print(Panel(rec.get("synthesis", "No synthesis saved."), title="[bold gold1]✦ ORACLE'S SYNTHESIS ✦[/bold gold1]", border_style="gold1"))
    press_to_continue()

def _export_record_to_markdown(rec: Dict[str, Any]):
    timestamp_safe = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tarot_reading_{timestamp_safe}.md"

    md_lines = [
        f"# 🔮 Tarot Divination Chronicle",
        f"**Date:** {rec.get('date_str')}",
        f"**Spread:** {rec.get('spread_name')}",
        f"**Inquiry:** {rec.get('inquiry')}\n",
        "---",
        "## 🎴 Drawn Arcanas\n"
    ]

    for card_data in rec.get("cards", []):
        c_name = card_data["card_name"]
        is_rev = card_data["is_reversed"]
        pos = card_data["position"]
        state = "Reversed [▼]" if is_rev else "Upright [▲]"
        kws = ", ".join(card_data.get("keywords", []))
        md_lines.append(f"### {pos}: **{c_name}** ({state})")
        md_lines.append(f"- **Keywords:** {kws}\n")

    md_lines.append("---\n## 🌌 Oracle's Grand Prophecy\n")
    md_lines.append(rec.get("synthesis", ""))
    md_lines.append("\n\n*Inscribed by Arcana: Veil of Destiny*")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    console.print(f"\n[bold green]✦ Reading successfully exported to '{filename}'! ✦[/bold green]")
    press_to_continue()

def browse_card_codex():
    """Interactive card encyclopedia for all 78 Tarot cards."""
    while True:
        console.clear()
        console.print("[bold gold1]═══════════ THE SACRED CODEX OF 78 ARCANAS ═══════════[/bold gold1]\n")
        console.print("Browse the esoteric lore, archetypes, and dual orientations of any card.\n")

        choice = ask_choice(
            "Select Codex Realm to Explore:",
            [
                "Major Arcana (The 22 Archetypes of the Soul's Journey)",
                "Suit of Wands (Fire / Will & Passion)",
                "Suit of Cups (Water / Love & Intuition)",
                "Suit of Swords (Air / Mind & Truth)",
                "Suit of Pentacles (Earth / Material & Body)",
                "Search Card by Name directly",
                "Return to Main Menu"
            ]
        )

        if choice == 1:
            _browse_card_list(MAJOR_ARCANA, "Major Arcana")
        elif choice == 2:
            wands = [c for c in MINOR_ARCANA if c.suit == "Wands"]
            _browse_card_list(wands, "Suit of Wands")
        elif choice == 3:
            cups = [c for c in MINOR_ARCANA if c.suit == "Cups"]
            _browse_card_list(cups, "Suit of Cups")
        elif choice == 4:
            swords = [c for c in MINOR_ARCANA if c.suit == "Swords"]
            _browse_card_list(swords, "Suit of Swords")
        elif choice == 5:
            pentacles = [c for c in MINOR_ARCANA if c.suit == "Pentacles"]
            _browse_card_list(pentacles, "Suit of Pentacles")
        elif choice == 6:
            query = Prompt.ask("[bold cyan]Enter card name (or partial name)[/bold cyan]").lower().strip()
            matches = [c for c in ALL_CARDS if query in c.name.lower()]
            if matches:
                _browse_card_list(matches, f"Search Results for '{query}'")
            else:
                console.print(f"[red]No card found matching '{query}'.[/red]")
                press_to_continue()
        else:
            break

def _browse_card_list(cards: List[Card], title: str):
    console.clear()
    console.print(f"[bold gold1]✦ CODEX: {title.upper()} ({len(cards)} Cards) ✦[/bold gold1]\n")
    
    options = [f"{c.numeral} {c.name} — {c.essence}" for c in cards]
    options.append("Back to Codex Realm Menu")

    choice = ask_choice("Select a card to examine in depth:", options)
    if choice <= len(cards):
        chosen = cards[choice - 1]
        _examine_card(chosen)

def _examine_card(card: Card):
    while True:
        console.clear()
        console.print(f"[bold gold1]═══════════ CODEX STUDY: {card.name.upper()} ═══════════[/bold gold1]\n")
        
        # Display both Upright and Reversed ASCII art side-by-side
        a_up = render_card_ascii(card, False)
        a_rev = render_card_ascii(card, True)
        
        from arcana.ascii_art import merge_cards_horizontal
        console.print("[bold green]      [▲ UPRIGHT FACE ▲]     [/bold green]          [bold red]     [▼ REVERSED FACE ▼]     [/bold red]")
        console.print(merge_cards_horizontal([a_up, a_rev], spacing=6))
        console.print()

        choice = ask_choice(
            f"Examine lore of {card.name}:",
            [
                "View Upright Lore & Prophecy",
                "View Reversed (Shadow) Lore & Warnings",
                "Return to List"
            ]
        )

        if choice == 1:
            console.clear()
            display_card_full_reading(card, False, "CODEX STUDY")
            press_to_continue()
        elif choice == 2:
            console.clear()
            display_card_full_reading(card, True, "CODEX STUDY")
            press_to_continue()
        else:
            break
