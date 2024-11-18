from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name if self.player.active_creature else 'None'}

Opponent's Team:
{bot_creatures_status}
Active: {self.bot.active_creature.display_name if self.bot.active_creature else 'None'}

> Attack
> Swap (if available)
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        # Get available choices
        choices = [Button("Attack")]
        
        # Only add swap if there are valid creatures to swap to
        available_creatures = [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            skills = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skills)
        else:
            swap_choices = [SelectThing(c) for c in available_creatures]
            return self._wait_for_choice(player, swap_choices)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You swapped to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Opponent swapped to {bot_action.thing.display_name}!")

        # Then handle attacks
        actions = []
        if not isinstance(player_action.thing, Creature):
            actions.append((self.player, player_action.thing))
        if not isinstance(bot_action.thing, Creature):
            actions.append((self.bot, bot_action.thing))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    choices = [SelectThing(c) for c in available_creatures]
                    swap_choice = self._wait_for_choice(defender, choices)
                    defender.active_creature = swap_choice.thing
                    self._show_text(self.player, 
                        f"{'You' if defender == self.player else 'Opponent'} swapped to {swap_choice.thing.display_name}!")

    def execute_skill(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{'You' if attacker == self.player else 'Opponent'} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
