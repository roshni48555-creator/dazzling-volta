"""
The Fate Weaver: Interactive Tarot Narrative RPG Mode.
An atmospheric mystical text journey where your choices and real Tarot card draws
(both Upright and Reversed) determine your path, trial resolutions, and soul fate.
"""
import time
import random
from typing import Dict, List, Tuple
from rich.panel import Panel
from rich.text import Text

from arcana.display import console, typewrite, animate_card_reveal, ask_choice, press_to_continue
from arcana.engine import TarotDeck
from arcana.cards_data import Card
from arcana import sound

class FateWeaverRPG:
    def __init__(self):
        self.deck = TarotDeck()
        self.deck.shuffle_riffle()
        self.karma = 0
        self.light_resonance = 10
        self.shadow_insight = 10
        self.fate_affinity = 10
        self.inventory: List[str] = ["Silver Amulet of the Veil", "Vial of Sacred Starlight"]
        self.drawn_chronicle: List[Tuple[str, Card, bool]] = []

    def run(self):
        console.clear()
        sound.play_omen_bell()
        
        intro_text = Text()
        intro_text.append("✦ CHAPTER 0: THE CROSSROADS OF THE MIST ✦\n\n", style="bold magenta")
        intro_text.append(
            "You awaken with dew upon your brow at the junction of four ancient marble paths.\n"
            "Above, the sky is neither night nor day, but an iridescent twilight patterned with silver constellations.\n"
            "Before you stands a cloaked figure whose face is masked by a veil woven from black silk and stardust.\n"
            "'Welcome, Wanderer,' whispers the Veiled Guide. 'You stand before the Loom of the Fates.\n"
            "Here, your path is not merely chosen—it is drawn from the living deck of the 78 Arcanas.\n"
            "Every card pulled may shine upright with virtue, or turn inverted into the trials of the shadow.'\n",
            style="italic bright_white"
        )
        console.print(Panel(intro_text, title="[bold gold1]✦ THE FATE WEAVER: CHRONICLES OF THE VEIL ✦[/bold gold1]", border_style="magenta"))
        press_to_continue("Press Enter to step onto the path...")

        # Chapter 1: The Gate of Fire
        self._chapter_1_the_gate_of_fire()

        # Chapter 2: The Marsh of the Deep Mirror
        self._chapter_2_the_marsh_of_reflection()

        # Chapter 3: The Citadel of Iron Scales
        self._chapter_3_the_citadel_of_scales()

        # Chapter 4: The Apex of the Starweaver
        self._chapter_4_the_apex_climax()

        # Final Epilogue and Fate Evaluation
        self._epilogue()

    def _chapter_1_the_gate_of_fire(self):
        console.clear()
        console.print("[bold gold1]═══════════ CHAPTER I: THE ARCHWAY OF EMBERS ═══════════[/bold gold1]\n")
        typewrite(
            "The marble road leads you toward a monolithic arch carved of blackened basalt. Glowing coals pulse beneath its threshold,\n"
            "and crimson runes flare along its stones. A guardian sphinx of obsidian blocks the passageway, its eyes burning like torches.\n"
            "'None may enter without offering their guiding principle to the fire,' the guardian rumbles.\n"
            "The Veiled Guide steps forward, extending the deck of cards: 'Draw, Traveler. Let destiny reveal your key.'\n"
        )
        
        press_to_continue("Press Enter to draw your Key from the Veil...")
        card, is_rev = self.deck.draw_top()
        self.drawn_chronicle.append(("Chapter 1: The Archway of Embers", card, is_rev))
        animate_card_reveal(card, is_rev, "YOUR DRAWN KEY")

        meaning = card.reversed if is_rev else card.upright
        console.print(f"[bold cyan]✦ The Sphinx observes {card.name} ({'Reversed' if is_rev else 'Upright'}) ✦[/bold cyan]")
        console.print(f"[dim italic]Archetype: {meaning.archetype} — {', '.join(meaning.keywords[:3])}[/dim italic]\n")

        if not is_rev:
            console.print("[bold green]The card blazes with pure upright radiance![/bold green]")
            choice = ask_choice(
                "How do you channel this upright virtue before the guardian?",
                [
                    f"Present {card.name}'s blessing with fearless authority (+Light Resonance, +Fate Affinity)",
                    f"Offer the card's wisdom as an intellectual riddle to outsmart the Sphinx (+Shadow Insight, +Light)",
                    f"Absorb the card's elemental power directly into your spirit (+Light Resonance)"
                ]
            )
            if choice == 1:
                self.light_resonance += 15
                self.fate_affinity += 10
                typewrite("\nThe Sphinx bows its massive stone head: 'The purity of your intent clears the flame.' The coals part peacefully.\n")
            elif choice == 2:
                self.shadow_insight += 10
                self.light_resonance += 10
                typewrite("\nThe Sphinx lets out a rumbling laugh: 'Few mortals answer flame with riddle. You may pass.'\n")
            else:
                self.light_resonance += 20
                typewrite("\nA surge of warmth flows into your veins. The embers beneath your feet turn into harmless rose petals.\n")
        else:
            console.print("[bold red]The card turns upside down! The shadow challenge awakens![/bold red]")
            typewrite(f"The Sphinx scowls: 'The inverted mirror of {card.name}! A trial of shadow tests your mettle.'\n")
            choice = ask_choice(
                "How do you navigate this inverted omen?",
                [
                    f"Acknowledge the shadow weakness ({meaning.keywords[0]}) with humble confession (+Shadow Insight, +Fate Affinity)",
                    f"Use your Silver Amulet to balance the reversed energy into poise (+Light Resonance, -Inventory)",
                    f"Face the burning trial head-on with stubborn grit (+Fate Affinity, but taking the brunt of heat)"
                ]
            )
            if choice == 1:
                self.shadow_insight += 20
                self.fate_affinity += 10
                typewrite("\n'Humility in the face of shadow is the mark of true wisdom,' the Sphinx speaks, letting you cross unburned.\n")
            elif choice == 2:
                self.light_resonance += 15
                if "Silver Amulet of the Veil" in self.inventory:
                    self.inventory.remove("Silver Amulet of the Veil")
                typewrite("\nYour amulet shatters, absorbing the dark heat! The path opens, though your charm is spent.\n")
            else:
                self.fate_affinity += 5
                self.shadow_insight += 10
                typewrite("\nYou press through the searing coals, bearing the heat with clenched teeth. You survive, tempered like steel.\n")

        press_to_continue()

    def _chapter_2_the_marsh_of_reflection(self):
        console.clear()
        console.print("[bold cyan]═══════════ CHAPTER II: THE WELL OF DROWNED MIRRORS ═══════════[/bold cyan]\n")
        typewrite(
            "Beyond the archway lies a tranquil, silver marsh shrouded in moonlit fog.\n"
            "In the center of the dark pool rests an ancient stone font. Floating upon the black water are visions\n"
            "of people from your past—faces of loved ones, former betrayers, and forgotten dreams.\n"
            "The Guide cautions: 'This water reveals the illusion that binds your heart. Draw from the deck to uncover what waits in the depths.'\n"
        )
        
        press_to_continue("Press Enter to draw the Mirror Card...")
        card, is_rev = self.deck.draw_top()
        self.drawn_chronicle.append(("Chapter 2: The Well of Drowned Mirrors", card, is_rev))
        animate_card_reveal(card, is_rev, "THE MIRROR REFLECTION")

        meaning = card.reversed if is_rev else card.upright
        console.print(f"[bold cyan]✦ The pool ripples beneath {card.name} ({'Reversed' if is_rev else 'Upright'}) ✦[/bold cyan]")
        console.print(f"[dim italic]Reflection: {meaning.prophecy}[/dim italic]\n")

        if not is_rev:
            choice = ask_choice(
                "How will you embrace the revelation in the water?",
                [
                    "Forgive the past completely and send a blessing into the pool (+Light Resonance)",
                    "Harvest the sacred lotus of wisdom blooming upon the surface (+Fate Affinity, +Shadow Insight)",
                    "Pour your Vial of Starlight into the pool to illuminate the whole marsh (+Light Resonance, +All)"
                ]
            )
            if choice == 1:
                self.light_resonance += 15
                typewrite("\nThe dark water turns clear as diamond. The spirits in the pool smile and dissolve into starlight.\n")
            elif choice == 2:
                self.shadow_insight += 15
                self.fate_affinity += 10
                self.inventory.append("Lotus of Clear Sight")
                typewrite("\nYou pluck the crystal lotus; its petals grant you piercing intuitive discernment.\n")
            else:
                self.light_resonance += 20
                self.fate_affinity += 15
                if "Vial of Sacred Starlight" in self.inventory:
                    self.inventory.remove("Vial of Sacred Starlight")
                typewrite("\nThe entire marsh erupts in celestial luminescence! The fog vanishes, revealing a stairway of pure moonstone.\n")
        else:
            typewrite(f"[bold red]An eerie illusion arises from the inverted {card.name}![/bold red] The shadows grasp at your reflection.\n")
            choice = ask_choice(
                "How do you dispel the dark mirage?",
                [
                    f"Refuse the illusion: confront the hidden wound ({meaning.keywords[0]}) without flinching (+Shadow Insight)",
                    "Close your eyes and walk through the marsh guided purely by inner instinct (+Fate Affinity)",
                    "Cast a stone into the center to shatter the deceptive reflection (+Light Resonance)"
                ]
            )
            if choice == 1:
                self.shadow_insight += 20
                typewrite("\nAs you name your shadow, the grasping specters lose their form and turn into gentle ripples.\n")
            elif choice == 2:
                self.fate_affinity += 15
                self.light_resonance += 10
                typewrite("\nTrusting the darkness, your feet find invisible stones. You emerge upon the far bank unharmed.\n")
            else:
                self.light_resonance += 10
                typewrite("\nThe ripples shatter the illusion, granting you just enough time to scramble across the wet stones.\n")

        press_to_continue()

    def _chapter_3_the_citadel_of_scales(self):
        console.clear()
        console.print("[bold yellow]═══════════ CHAPTER III: THE CITADEL OF IRON SCALES ═══════════[/bold yellow]\n")
        typewrite(
            "You ascend high into the jagged crags where the Citadel of Iron Scales overlooks the abyss.\n"
            "Here sits the High Magistrate of Karma, an ethereal judge crowned with iron stars, holding golden scales.\n"
            "'You have walked through fire and water,' declares the Magistrate. 'Now your moral integrity is weighed.\n"
            "Will your actions tip the scale toward selfish conquest, or toward the liberation of all who wander here?'\n"
        )
        
        press_to_continue("Press Enter to draw the Card of Judgment...")
        card, is_rev = self.deck.draw_top()
        self.drawn_chronicle.append(("Chapter 3: The Citadel of Iron Scales", card, is_rev))
        animate_card_reveal(card, is_rev, "THE SCALES OF KARMA")

        meaning = card.reversed if is_rev else card.upright
        console.print(f"[bold cyan]✦ The Magistrate places {card.name} ({'Reversed' if is_rev else 'Upright'}) upon the scale ✦[/bold cyan]\n")

        if not is_rev:
            typewrite(f"The golden pan rises effortlessly under the upright weight of {card.name}.\n")
            choice = ask_choice(
                "The Magistrate offers you a blessing. What do you request?",
                [
                    "The Crown of Sovereign Truth (Mastery over your worldly purpose, +Light Resonance)",
                    "The Eye of the Unseen (Mastery over secrets, lies, and occult discernment, +Shadow Insight)",
                    "The Blessing of the Open Loom (Freedom to rewrite one tragic event in your chronicle, +Fate Affinity)"
                ]
            )
            if choice == 1:
                self.light_resonance += 25
            elif choice == 2:
                self.shadow_insight += 25
            else:
                self.fate_affinity += 25
        else:
            typewrite(f"[bold red]The scale groans heavily under the inverted burden of {card.name}![/bold red]\n")
            typewrite("The Magistrate leans forward: 'A karmic debt or blind spot hangs in the balance.'\n")
            choice = ask_choice(
                "How do you square this debt?",
                [
                    f"Offer voluntary penance: accept the lesson of {meaning.keywords[0]} (+Fate Affinity, +Shadow Insight)",
                    "Argue your case using sharp logic and intellect (+Light Resonance, +Shadow Insight)",
                    "Pledge your service to guide the next wanderer who enters the Veil (+Light Resonance, +Fate Affinity)"
                ]
            )
            if choice == 1:
                self.fate_affinity += 20
                self.shadow_insight += 15
            elif choice == 2:
                self.light_resonance += 10
                self.shadow_insight += 20
            else:
                self.light_resonance += 25
                self.fate_affinity += 20

        press_to_continue()

    def _chapter_4_the_apex_climax(self):
        console.clear()
        console.print("[bold magenta]═══════════ CHAPTER IV: THE APEX OF THE STARWEAVER ═══════════[/bold magenta]\n")
        typewrite(
            "You reach the summit of the universe: the Great Cosmic Loom.\n"
            "Before you, threads of spun starlight, golden solar fiber, and obsidian shadow interlace into the tapestry of all reality.\n"
            "The Veiled Guide drops their cloak—revealing that the Guide was your own higher self all along!\n"
            "'The final thread must now be drawn,' your Higher Self speaks. 'This card will seal your destiny.'\n"
        )
        
        press_to_continue("Press Enter to draw the Final Destined Arcana...")
        card, is_rev = self.deck.draw_top()
        self.drawn_chronicle.append(("Chapter 4: The Apex of the Starweaver", card, is_rev))
        animate_card_reveal(card, is_rev, "THE SEAL OF DESTINY")

        meaning = card.reversed if is_rev else card.upright
        console.print(f"[bold gold1]✦ THE FINAL THREAD: {card.name.upper()} ({'REVERSED' if is_rev else 'UPRIGHT'}) ✦[/bold gold1]")
        console.print(f"[italic white]{meaning.prophecy}[/italic white]\n")

        if not is_rev:
            self.light_resonance += 25
            self.fate_affinity += 25
            sound.play_victory()
        else:
            self.shadow_insight += 30
            self.fate_affinity += 20
            sound.play_omen_bell()

        press_to_continue("Press Enter to witness your final Fate Epitaph...")

    def _epilogue(self):
        console.clear()
        console.print("[bold gold1]═══════════════ THE VEIL OF DESTINY: EPILOGUE ═══════════════[/bold gold1]\n")
        
        # Determine ending based on stats
        total_score = self.light_resonance + self.shadow_insight + self.fate_affinity
        
        console.print(f"[bold cyan]✦ FINAL SOUL RESONANCE ✦[/bold cyan]")
        console.print(f"  ☀️  Light Resonance: [bold green]{self.light_resonance}[/bold green]")
        console.print(f"  🌑  Shadow Insight:   [bold magenta]{self.shadow_insight}[/bold magenta]")
        console.print(f"  ☸️   Fate Harmony:     [bold yellow]{self.fate_affinity}[/bold yellow]")
        console.print(f"  ✨ Total Soul Power: [bold gold1]{total_score}[/bold gold1]\n")

        # Chronicle Table
        console.print("[bold gold1]📜 YOUR ODYSSEY CHRONICLE:[/bold gold1]")
        for ch_title, card, is_rev in self.drawn_chronicle:
            state = "[bold red]Reversed [▼][/bold red]" if is_rev else "[bold green]Upright [▲][/bold green]"
            console.print(f"  • {ch_title}: [bold white]{card.name}[/bold white] ({state})")
        console.print()

        # Ending path
        if self.light_resonance >= self.shadow_insight + 15:
            title = "THE SOVEREIGN OF SOLAR DAWN"
            desc = (
                "You step into the Loom as a bearer of radiant light. The shadows of past doubt dissolve in your presence. "
                "You return to the mortal realm empowered to heal, lead, and illuminate the lives of everyone you touch."
            )
            color = "bold gold1"
        elif self.shadow_insight >= self.light_resonance + 15:
            title = "THE MASTER OF THE ECLIPSE & OCCULT VEILS"
            desc = (
                "You have stared into the dark mirror and neither flinched nor fell. You walk with the wisdom of the shadows, "
                "immune to deception, possessing piercing psychological insight and the rare ability to transmute sorrow into gold."
            )
            color = "bold magenta"
        elif self.fate_affinity >= 50:
            title = "THE ALCHEMICAL WEAVER OF SACRED BALANCE"
            desc = (
                "You have achieved the supreme ideal of the Tarot: total equilibrium between light and shadow, upright virtue "
                "and inverted wisdom. You understand that night and day are two wings of the same celestial eagle. The Loom bends to your gentle will."
            )
            color = "bold cyan"
        else:
            title = "THE ENLIGHTENED PILGRIM"
            desc = (
                "You return from the Veil forever changed. You carry the cards not as fixed commands, but as a living compass. "
                "Your journey has only just begun."
            )
            color = "bold white"

        panel = Panel(
            f"[{color}][size=16]✦ {title} ✦[/size][/{color}]\n\n"
            f"[bright_white]{desc}[/bright_white]\n\n"
            f"[dim italic]'Remember, Wanderer: The stars impel, they do not compel.'[/dim italic]",
            border_style=color.split()[-1],
            padding=(1, 2)
        )
        console.print(panel)
        sound.play_omen_bell()
        press_to_continue("Press Enter to return to the Sanctum Menu...")
