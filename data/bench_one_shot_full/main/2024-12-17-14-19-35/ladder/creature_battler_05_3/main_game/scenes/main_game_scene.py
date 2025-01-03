from typing import List, Optional
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        # Reset creature HPs
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.hp} HP" 
            for c in self.bot.creatures
        )
        return f"""=== Battle ===
Your Active Creature: {self.player.active_creature.display_name} ({self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP)
Foe's Active Creature: {self.bot.active_creature.display_name} ({self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP)

Your Team:
{player_creatures_status}

Foe's Team:
{bot_creatures_status}
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn(self, first_player: Player, second_player: Player):
        # Get actions from both players
        first_action = self._get_player_action(first_player)
        second_action = self._get_player_action(second_player)

        # Handle swaps first
        if isinstance(first_action, Creature):
            first_player.active_creature = first_action
        if isinstance(second_action, Creature):
            second_player.active_creature = second_action

        # Handle attacks
        if isinstance(first_action, Skill):
            damage = self._calculate_damage(first_player.active_creature, second_player.active_creature, first_action)
            second_player.active_creature.hp -= damage
            self._show_text(first_player, f"{first_player.active_creature.display_name} used {first_action.display_name}!")
            self._show_text(second_player, f"{first_player.active_creature.display_name} used {first_action.display_name}!")

        if isinstance(second_action, Skill) and second_player.active_creature.hp > 0:
            damage = self._calculate_damage(second_player.active_creature, first_player.active_creature, second_action)
            first_player.active_creature.hp -= damage
            self._show_text(first_player, f"{second_player.active_creature.display_name} used {second_action.display_name}!")
            self._show_text(second_player, f"{second_player.active_creature.display_name} used {second_action.display_name}!")

    def _get_player_action(self, player: Player) -> Skill | Creature:
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            available_creatures = self._get_available_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if isinstance(choice, Button):
                    continue  # Go back to main menu
                return choice.thing
            else:
                # Show available creatures with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if isinstance(choice, Button):
                    continue  # Go back to main menu
                return choice.thing

    def _handle_knockouts(self, player: Player):
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
            
            creature_choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            
        return True

    def run(self):
        while True:
            # Determine turn order based on speed
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed > bot_speed:
                self._handle_turn(self.player, self.bot)
            elif bot_speed > player_speed:
                self._handle_turn(self.bot, self.player)
            else:
                # Equal speeds - random order
                first_player, second_player = random.choice([
                    (self.player, self.bot),
                    (self.bot, self.player)
                ])
                self._handle_turn(first_player, second_player)

            # Check for knockouts
            player_can_continue = self._handle_knockouts(self.player)
            bot_can_continue = self._handle_knockouts(self.bot)

            if not player_can_continue:
                self._show_text(self.player, "You lost the battle!")
                break
            elif not bot_can_continue:
                self._show_text(self.player, "You won the battle!")
                break

        self._transition_to_scene("MainMenuScene")
