from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
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
{"> Swap" if self._get_available_creatures(p1) else ""}
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
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

        return int(raw_damage * effectiveness)

    def _get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_fainted(self, player: Player):
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
            
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _get_player_action(self):
        while True:
            # Main choice
            choices = [Button("Attack")]
            available_creatures = self._get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(self.player, choices)

            if isinstance(main_choice, Button) and main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                
                if isinstance(skill_choice, Button):
                    continue
                return ("attack", skill_choice.thing)
            else:
                # Show creatures with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                
                if isinstance(creature_choice, Button):
                    continue
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self._get_player_action()

            # Foe Choice Phase
            bot_action = None
            available_bot_creatures = self._get_available_creatures(self.bot)
            if not available_bot_creatures or random.random() < 0.8:  # 80% chance to attack or no choice
                bot_action = ("attack", random.choice(self.bot.active_creature.skills))
            else:
                bot_action = ("swap", random.choice(available_bot_creatures))

            # Resolution Phase
            # Handle swaps first
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
            if bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]

            # Handle attacks
            if player_action[0] == "attack" and bot_action[0] == "attack":
                # Determine order with random resolution for speed ties
                if self.player.active_creature.speed == self.bot.active_creature.speed:
                    first = random.choice([self.player, self.bot])
                else:
                    first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
                second = self.bot if first == self.player else self.player
                first_action = player_action if first == self.player else bot_action
                second_action = bot_action if first == self.player else player_action

                # First attack
                damage = self._calculate_damage(first.active_creature, second.active_creature, first_action[1])
                second.active_creature.hp -= damage
                self._show_text(self.player, f"{first.active_creature.display_name} used {first_action[1].display_name}!")
                
                if second.active_creature.hp > 0:
                    # Second attack
                    damage = self._calculate_damage(second.active_creature, first.active_creature, second_action[1])
                    first.active_creature.hp -= damage
                    self._show_text(self.player, f"{second.active_creature.display_name} used {second_action[1].display_name}!")

            # Check for fainted creatures
            if not self._handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self._handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
