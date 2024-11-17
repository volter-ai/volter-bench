from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
{"> Swap" if len(self.get_available_creatures(p1)) > 0 else ""}
"""

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def execute_skill(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def handle_knocked_out(self, player):
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
            
            choices = [SelectThing(c) for c in available]
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def get_player_action(self):
        while True:
            # Build available choices
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            # Main choice
            choice = self._wait_for_choice(self.player, choices)

            if isinstance(choice, Button) and choice.display_name == "Attack":
                # Attack submenu
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                
                if isinstance(skill_choice, Button):
                    continue
                return ("attack", skill_choice.thing)
            else:
                # Swap submenu
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                
                if isinstance(creature_choice, Button):
                    continue
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player turn with Back option support
            player_action = self.get_player_action()

            # Bot turn
            bot_action = ("attack", random.choice(self.bot.active_creature.skills))

            # Resolution
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
                self._show_text(self.player, f"{self.player.display_name} swapped to {player_action[1].display_name}!")
                self.execute_skill(self.bot.active_creature, self.player.active_creature, bot_action[1])
            elif bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]
                self._show_text(self.player, f"{self.bot.display_name} swapped to {bot_action[1].display_name}!")
                self.execute_skill(self.player.active_creature, self.bot.active_creature, player_action[1])
            else:
                # Both used attacks - check speed
                if self.player.active_creature.speed > self.bot.active_creature.speed or \
                   (self.player.active_creature.speed == self.bot.active_creature.speed and random.random() < 0.5):
                    self.execute_skill(self.player.active_creature, self.bot.active_creature, player_action[1])
                    if self.bot.active_creature.hp > 0:
                        self.execute_skill(self.bot.active_creature, self.player.active_creature, bot_action[1])
                else:
                    self.execute_skill(self.bot.active_creature, self.player.active_creature, bot_action[1])
                    if self.player.active_creature.hp > 0:
                        self.execute_skill(self.player.active_creature, self.bot.active_creature, player_action[1])

            # Check for knocked out creatures
            if not self.handle_knocked_out(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self.handle_knocked_out(self.bot):
                self._show_text(self.player, "You won!")
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
