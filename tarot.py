#!/usr/bin/env python3
"""
ARCANA: VEIL OF DESTINY
The Definitive Mystical CLI Tarot Game & Divination Engine
"""
import sys
import os

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    os.system("")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

from arcana.display import (
    console, print_banner, ask_choice, press_to_continue,
    set_animation, ANIMATION_ENABLED
)
from arcana.engine import TarotDeck, DeckOrientationSetting
from arcana.sanctuary import run_divination_sanctuary
from arcana.game_rpg import FateWeaverRPG
from arcana.game_duel import TarotDuel
from arcana.celestial import run_celestial_alignment
from arcana.grimoire import browse_card_codex, view_reading_history
from arcana import sound

def settings_menu(deck: TarotDeck):
    """Allows configuring deck reversal rates, sound, and animations."""
    global ANIMATION_ENABLED
    while True:
        console.clear()
        console.print("[bold gold1]═══════════ SANCTUM SANCTORUM SETTINGS ═══════════[/bold gold1]\n")
        
        sound_status = "ENABLED [🔊]" if sound.SOUND_ENABLED else "MUTED [🔇]"
        anim_status = "ENABLED [✨]" if ANIMATION_ENABLED else "INSTANT [⚡]"

        console.print(f"Current Reversal Mode: [bold cyan]{deck.reversal_setting}[/bold cyan]")
        console.print(f"Current Sound Effects: [bold magenta]{sound_status}[/bold magenta]")
        console.print(f"Current Animations:    [bold yellow]{anim_status}[/bold yellow]\n")

        choice = ask_choice(
            "Configure Preferences:",
            [
                "Change Reversal Orientation Probability",
                f"Toggle Sound Effects (Currently {sound_status})",
                f"Toggle Visual Animations (Currently {anim_status})",
                "Return to Main Sanctum Menu"
            ]
        )

        if choice == 1:
            rev_choice = ask_choice(
                "Select Tarot Reversal Philosophy:",
                [
                    DeckOrientationSetting.BALANCED,
                    DeckOrientationSetting.GENTLE,
                    DeckOrientationSetting.SHADOW,
                    DeckOrientationSetting.UPRIGHT_ONLY
                ]
            )
            settings = [
                DeckOrientationSetting.BALANCED,
                DeckOrientationSetting.GENTLE,
                DeckOrientationSetting.SHADOW,
                DeckOrientationSetting.UPRIGHT_ONLY
            ]
            deck.set_reversal_mode(settings[rev_choice - 1])
            console.print(f"\n[bold green]✦ Reversal mode updated to {deck.reversal_setting}! ✦[/bold green]")
            press_to_continue()
        elif choice == 2:
            new_state = sound.toggle_sound()
            console.print(f"\n[bold green]✦ Sound is now {'ENABLED' if new_state else 'MUTED'}! ✦[/bold green]")
            if new_state:
                sound.play_reveal()
            press_to_continue()
        elif choice == 3:
            ANIMATION_ENABLED = not ANIMATION_ENABLED
            set_animation(ANIMATION_ENABLED)
            console.print(f"\n[bold green]✦ Animations are now {'ENABLED' if ANIMATION_ENABLED else 'INSTANT'}! ✦[/bold green]")
            press_to_continue()
        else:
            break

def main():
    deck = TarotDeck()
    deck.shuffle_riffle()

    while True:
        console.clear()
        print_banner()

        choice = ask_choice(
            "Choose your Sacred Passage:",
            [
                "🌌 The Divination Sanctuary (Grand Spreads: 1-Card, Trinity, Celtic Cross, etc.)",
                "📖 The Fate Weaver RPG (Narrative Tarot Quest with Real Card Draws)",
                "⚔️  The Duel of Mirrors (Tarot Card Combat vs the Shadow Doppelganger)",
                "🪐 Celestial Horoscope & Daily Oracle (Zodiac Alignments & Today's Card)",
                "📜 The Sacred Codex (Browse 78 Cards, Esoteric Lore & Inverted Meanings)",
                "🕯️ The Chronicle Journal (View Past Prophecies & Export to Markdown)",
                "⚙️  Sanctum Settings (Reversal Rates, Audio Chimes, Visual Pace)",
                "🚪 Depart the Veil (Exit)"
            ]
        )

        if choice == 1:
            run_divination_sanctuary(deck)
        elif choice == 2:
            game = FateWeaverRPG()
            game.run()
        elif choice == 3:
            duel = TarotDuel()
            duel.run()
        elif choice == 4:
            run_celestial_alignment()
        elif choice == 5:
            browse_card_codex()
        elif choice == 6:
            view_reading_history()
        elif choice == 7:
            settings_menu(deck)
        else:
            console.clear()
            console.print("[bold gold1]May the stars illuminate your steps until the Veil calls you again.[/bold gold1]\n")
            sound.play_omen_bell()
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]The Veil gently closes...[/dim]")
        sys.exit(0)
