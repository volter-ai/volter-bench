from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap (if you have available creatures)
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

    def _get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn(self, player, opponent):
        # Build choice list based on available options
        choices = [Button("Attack")]
        
        # Only add swap option if there are creatures to swap to
        available_creatures = self._get_available_creatures(player)
        if available_creatures:
            choices.append(Button("Swap"))

        choice = self._wait_for_choice(player, choices)

        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choice = self._wait_for_choice(player, skill_choices)
            return ("attack", skill_choice.thing)
        else:
            # Show available creatures
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            return ("swap", creature_choice.thing)

    def _execute_turn(self, player_action, bot_action):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature

        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            player_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            bot_creature = bot_action[1]

        # Execute attacks in speed order
        if player_action[0] == "attack" and bot_action[0] == "attack":
            first = self.player if player_creature.speed >= bot_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action

            # First attack
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action[1])
            second.active_creature.hp -= damage
            self._show_text(first, f"{first.active_creature.display_name} used {first_action[1].display_name}!")
            self._show_text(second, f"Took {damage} damage!")

            # Second attack if still alive
            if second.active_creature.hp > 0:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_action[1])
                first.active_creature.hp -= damage
                self._show_text(second, f"{second.active_creature.display_name} used {second_action[1].display_name}!")
                self._show_text(first, f"Took {damage} damage!")

    def _check_for_fainted(self, player):
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
            
            creature_choices = [SelectThing(c) for c in available]
            self._show_text(player, f"{player.active_creature.display_name} fainted!")
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            
        return True

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player, self.bot)
            
            # Bot turn
            bot_action = self._handle_turn(self.bot, self.player)
            
            # Execute turn
            self._execute_turn(player_action, bot_action)
            
            # Check for fainted creatures
            player_can_continue = self._check_for_fainted(self.player)
            bot_can_continue = self._check_for_fainted(self.bot)
            
            if not player_can_continue:
                self._show_text(self.player, "You lost!")
                break
            elif not bot_can_continue:
                self._show_text(self.player, "You won!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
