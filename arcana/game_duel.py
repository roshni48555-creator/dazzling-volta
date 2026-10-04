"""
The Duel of Mirrors: Strategic Tarot Battle Minigame.
Engage in esoteric psychic combat against the Shadow Doppelganger using Tarot cards.
Upright cards unleash radiant virtues; Reversed cards cast forbidden hexes and inversions!
"""
import random
import time
from typing import List, Tuple, Dict, Optional
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from arcana.display import console, ask_choice, press_to_continue, typewrite
from arcana.cards_data import ALL_CARDS, Card
from arcana.engine import TarotDeck
from arcana.ascii_art import render_card_ascii, merge_cards_horizontal
from arcana import sound

class DuelFighter:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.is_ai = is_ai
        self.hp = 100
        self.max_hp = 100
        self.shield = 0
        self.hand: List[Tuple[Card, bool]] = []
        self.mirror_flips_remaining = 1  # Ability to invert a card in hand

    def take_damage(self, amount: int) -> int:
        absorbed = min(self.shield, amount)
        self.shield -= absorbed
        remaining = amount - absorbed
        self.hp = max(0, self.hp - remaining)
        return amount

    def gain_shield(self, amount: int):
        self.shield = min(50, self.shield + amount)

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

def calculate_card_combat_effect(card: Card, is_rev: bool) -> Tuple[str, int, int, str]:
    """
    Returns:
    (effect_type, damage_dealt, shield_or_heal_amount, description)
    """
    suit = card.suit
    rank = card.rank

    # Major Arcana custom powers
    if card.arcana == "Major":
        if "Magician" in card.name:
            if not is_rev:
                return ("attack", 26, 0, "Alchemical Blast: Blasts pure raw elements for 26 damage!")
            else:
                return ("drain", 18, 12, "Forbidden Sleight: Drains 18 HP and absorbs 12 health!")
        elif "Tower" in card.name:
            if not is_rev:
                return ("cataclysm", 35, 0, "Cataclysmic Bolt: Lightning crashes down for 35 catastrophic damage!")
            else:
                return ("shatter", 22, 0, "Rubble Crush: Shatters enemy wards and strikes for 22 damage!")
        elif "Star" in card.name:
            if not is_rev:
                return ("heal", 0, 32, "Celestial Nectar: Restores 32 vitality under starlight!")
            else:
                return ("debuff", 15, 10, "Extinguished Beacon: Weakens foe for 15 damage and heals 10!")
        elif "Sun" in card.name:
            if not is_rev:
                return ("solar", 30, 10, "Solar Flare: Blazes with 30 radiant damage and heals 10 HP!")
            else:
                return ("eclipse", 20, 10, "Solar Eclipse: Darkened rays inflict 20 damage and grant 10 shield!")
        elif "Death" in card.name:
            if not is_rev:
                return ("reap", 28, 0, "The Scythe's Sweep: Cuts through life force for 28 damage!")
            else:
                return ("resurrect", 0, 25, "Undying Phoenix: Refuses the grave and restores 25 HP!")
        elif "Devil" in card.name:
            if not is_rev:
                return ("chain", 24, 0, "Obsidian Chains: Binds the opponent for 24 shadow damage!")
            else:
                return ("breakfree", 20, 15, "Shattered Bonds: Breaks free dealing 20 damage and gaining 15 shield!")
        else:
            # General Major
            dmg = 22 if not is_rev else 18
            heal = 8 if not is_rev else 12
            return ("major_arcane", dmg, heal, f"Great Arcana Surge of {card.name}: Inflicts {dmg} damage and bolsters {heal} resilience!")

    # Minor Arcana by suit
    if suit == "Wands":
        if not is_rev:
            return ("fire", 22, 0, f"Blaze of Wands: Fierce flame strike dealing 22 fire damage!")
        else:
            return ("wildfire", 28, 0, f"Wildfire Inversion: Deals 28 damage in a reckless burst of flame!")
    elif suit == "Cups":
        if not is_rev:
            return ("water", 0, 26, f"Chalice of Rejuvenation: Heals 26 health from the sacred well.")
        else:
            return ("siphon", 16, 14, f"Dark Tides: Siphons 16 HP from the opponent and restores 14 HP!")
    elif suit == "Swords":
        if not is_rev:
            return ("air", 24, 0, f"Razor Severance: Slices through armor for 24 pure piercing damage!")
        else:
            return ("counter", 18, 10, f"Inverted Riposte: Deals 18 counter damage and raises 10 guard!")
    elif suit == "Pentacles":
        if not is_rev:
            return ("earth", 8, 24, f"Granite Bulwark: Strikes for 8 damage and constructs 24 stone shield!")
        else:
            return ("alchemy", 14, 18, f"Transmuted Coin: Strikes for 14 damage and yields 18 shield!")

    return ("basic", 15, 0, f"Arcane Surge: Deals 15 damage.")

class TarotDuel:
    def __init__(self):
        self.deck = TarotDeck()
        self.deck.shuffle_riffle()
        self.player = DuelFighter("The Seeker", is_ai=False)
        self.shadow = DuelFighter("The Shadow Doppelganger", is_ai=True)
        self.turn = 1

    def run(self):
        console.clear()
        sound.play_omen_bell()

        intro = (
            "[bold magenta]✦ THE ASTRAL ARENA: DUEL OF MIRRORS ✦[/bold magenta]\n\n"
            "A pool of quicksilver rises between you and an exact, dark replica of yourself.\n"
            "The Doppelganger holds three cards from the astral deck in their shadowed hand.\n\n"
            "[bold cyan]RULES OF COMBAT:[/bold cyan]\n"
            "• Each turn, play 1 card from your 3-card hand.\n"
            "• [bold green]Upright Cards [▲][/bold green] channel divine virtues, strikes, or restorative blessings.\n"
            "• [bold red]Reversed Cards [▼][/bold red] cast forbidden hexes, siphons, and high-risk gambits.\n"
            "• You hold 1 [bold yellow]Mirror Prism[/bold yellow]: Flip any card in your hand upside down before playing it!\n"
            "• First to deplete the opponent's Fate Energy to 0 wins the duel."
        )
        console.print(Panel(intro, border_style="cyan"))
        press_to_continue("Press Enter to draw your opening hand...")

        # Draw 3 cards each
        for _ in range(3):
            self.player.hand.append(self.deck.draw_top())
            self.shadow.hand.append(self.deck.draw_top())

        while self.player.hp > 0 and self.shadow.hp > 0:
            self._execute_round()
            self.turn += 1

        self._conclude_duel()

    def _render_status(self):
        # Health & shield bars
        table = Table(title=f"✦ ASTRAL COMBAT — TURN {self.turn} ✦", title_style="bold gold1", expand=True)
        table.add_column("Fighter", style="bold white", width=25)
        table.add_column("Fate Health", style="bold green", width=30)
        table.add_column("Astral Shield", style="bold blue", width=20)

        p_hp_bar = "█" * (self.player.hp // 5) + "░" * ((self.player.max_hp - self.player.hp) // 5)
        s_hp_bar = "█" * (self.shadow.hp // 5) + "░" * ((self.shadow.max_hp - self.shadow.hp) // 5)

        table.add_row(
            f"👤 {self.player.name}",
            f"[{p_hp_bar}] {self.player.hp}/{self.player.max_hp}",
            f"🛡️  {self.player.shield}"
        )
        table.add_row(
            f"👥 {self.shadow.name}",
            f"[{s_hp_bar}] {self.shadow.hp}/{self.shadow.max_hp}",
            f"🛡️  {self.shadow.shield}"
        )
        console.print(table)
        console.print()

    def _execute_round(self):
        console.clear()
        self._render_status()

        # Display player's current hand
        console.print("[bold gold1]🎴 YOUR CURRENT HAND (Choose a card to cast):[/bold gold1]")
        hand_arts = [render_card_ascii(c, is_rev) for c, is_rev in self.player.hand]
        console.print(merge_cards_horizontal(hand_arts, spacing=2))
        console.print()

        # Options
        options = []
        for idx, (card, is_rev) in enumerate(self.player.hand, start=1):
            rev_label = "[bold red]Reversed [▼][/bold red]" if is_rev else "[bold green]Upright [▲][/bold green]"
            effect_type, dmg, shld, desc = calculate_card_combat_effect(card, is_rev)
            options.append(f"Cast {card.name} ({rev_label}) — {desc}")

        if self.player.mirror_flips_remaining > 0:
            options.append(f"🔮 Use Mirror Prism (Flip orientation of a card in hand) [1 remaining]")

        choice = ask_choice("What is your tactical action?", options)

        # Check if Mirror Prism selected
        if choice == len(options) and self.player.mirror_flips_remaining > 0:
            flip_sub_options = [f"Flip {c.name} ({'Reversed' if r else 'Upright'})" for c, r in self.player.hand]
            flip_choice = ask_choice("Which card will you invert?", flip_sub_options)
            target_c, target_r = self.player.hand[flip_choice - 1]
            self.player.hand[flip_choice - 1] = (target_c, not target_r)
            self.player.mirror_flips_remaining -= 1
            sound.play_card_flip()
            console.print(f"\n[bold magenta]✦ The Mirror Prism revolves! {target_c.name} is now {'Reversed' if not target_r else 'Upright'}! ✦[/bold magenta]")
            press_to_continue()
            # Re-execute round choice
            self._execute_round()
            return

        # Player plays chosen card
        chosen_card, chosen_rev = self.player.hand.pop(choice - 1)
        # Draw replacement card
        self.player.hand.append(self.deck.draw_top())

        # Shadow AI picks card
        shadow_choice_idx = random.randint(0, len(self.shadow.hand) - 1)
        shadow_card, shadow_rev = self.shadow.hand.pop(shadow_choice_idx)
        self.shadow.hand.append(self.deck.draw_top())

        # Animate Clashing Cards
        console.clear()
        console.print("[bold gold1]═══════════ THE SACRED ASTRAL CLASH ═══════════[/bold gold1]\n")
        
        c1_art = render_card_ascii(chosen_card, chosen_rev)
        c2_art = render_card_ascii(shadow_card, shadow_rev)
        
        console.print(f"[bold cyan]YOUR SPELL: {chosen_card.name}[/bold cyan]              [bold red]SHADOW SPELL: {shadow_card.name}[/bold red]")
        console.print(merge_cards_horizontal([c1_art, c2_art], spacing=6))
        console.print()

        sound.play_clash()
        time.sleep(0.5)

        # Resolve Player Spell
        _, p_dmg, p_heal_or_shield, p_desc = calculate_card_combat_effect(chosen_card, chosen_rev)
        console.print(f"[bold cyan]✦ You invoke {chosen_card.name}:[/bold cyan] {p_desc}")
        if p_dmg > 0:
            self.shadow.take_damage(p_dmg)
            console.print(f"  ⚡ Inflicted [bold red]{p_dmg}[/bold red] damage upon the Doppelganger!")
        if p_heal_or_shield > 0:
            if "heal" in p_desc.lower() or "nectar" in p_desc.lower() or "rejuvenation" in p_desc.lower() or "siphon" in p_desc.lower():
                self.player.heal(p_heal_or_shield)
                console.print(f"  💚 Restored [bold green]{p_heal_or_shield}[/bold green] health!")
            else:
                self.player.gain_shield(p_heal_or_shield)
                console.print(f"  🛡️  Conjured [bold blue]{p_heal_or_shield}[/bold blue] astral shield!")

        time.sleep(0.4)

        # Check if shadow defeated
        if self.shadow.hp <= 0:
            return

        # Resolve Shadow Spell
        _, s_dmg, s_heal_or_shield, s_desc = calculate_card_combat_effect(shadow_card, shadow_rev)
        console.print(f"\n[bold red]✦ Doppelganger unleashes {shadow_card.name}:[/bold red] {s_desc}")
        if s_dmg > 0:
            self.player.take_damage(s_dmg)
            console.print(f"  ⚡ You sustain [bold red]{s_dmg}[/bold red] damage!")
        if s_heal_or_shield > 0:
            if "heal" in s_desc.lower() or "nectar" in s_desc.lower() or "rejuvenation" in s_desc.lower() or "siphon" in s_desc.lower():
                self.shadow.heal(s_heal_or_shield)
                console.print(f"  💚 Doppelganger recovers [bold green]{s_heal_or_shield}[/bold green] health!")
            else:
                self.shadow.gain_shield(s_heal_or_shield)
                console.print(f"  🛡️  Doppelganger gains [bold blue]{s_heal_or_shield}[/bold blue] shield!")

        press_to_continue()

    def _conclude_duel(self):
        console.clear()
        if self.player.hp > 0 and self.shadow.hp <= 0:
            sound.play_victory()
            console.print("[bold gold1]═══════════════ TRIUMPH OF THE MIRROR ═══════════════[/bold gold1]\n")
            panel = Panel(
                "[bold green]✦ VICTORY OVER THE SHADOW! ✦[/bold green]\n\n"
                "The quicksilver pool shatters into ten thousand diamonds.\n"
                "The Shadow Doppelganger smiles, bows with deep respect, and merges back into your soul.\n"
                "By mastering both upright virtues and inverted hexes, you have integrated your shadow.\n"
                "You gain the title: [bold gold1]MASTER OF MIRRORS & ARCANAS[/bold gold1].",
                border_style="gold1",
                padding=(1, 2)
            )
            console.print(panel)
        else:
            sound.play_shadow_reveal()
            console.print("[bold red]═══════════════ ECLIPSED BY THE SHADOW ═══════════════[/bold red]\n")
            panel = Panel(
                "[bold red]✦ THE MIRROR OVERWHELMS YOU ✦[/bold red]\n\n"
                "Your Fate Energy dissipates into the astral mists.\n"
                "The Doppelganger places a gentle hand on your shoulder: 'To conquer the shadow, you must first know its contours.'\n"
                "You awaken back at the threshold, wiser and ready to duel again.",
                border_style="red",
                padding=(1, 2)
            )
            console.print(panel)

        press_to_continue("Press Enter to return to the Sanctum Menu...")
