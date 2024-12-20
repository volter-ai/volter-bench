from typing import Tuple, NamedTuple
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player

class PlayerAction(NamedTuple):
    player: Player
    action: SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your creatures: {[c.display_name for c in self.player.creatures]}
Foe's creatures: {[c.display_name for c in self.bot.creatures]}"""

    def run(self):
        while True:
            # Player turn
            player_action = PlayerAction(self.player, self.get_player_action(self.player))
            bot_action = PlayerAction(self.bot, self.get_player_action(self.bot))
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before leaving
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                    
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_available_creatures(self, player):
        """Get list of creatures that can be swapped to"""
        return [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]

    def get_player_action(self, player):
        while True:
            # Main choice phase
            choices = []
            choices.append(Button("Attack"))
            
            # Only show Swap if there are creatures to swap to
            available_creatures = self.get_available_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main choices
                return choice
            else:
                # Show creatures for swap with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main choices
                return choice

    def resolve_actions(self, player_action: PlayerAction, bot_action: PlayerAction):
        # Handle swaps first
        if isinstance(player_action.action.thing, Creature):
            self.player.active_creature = player_action.action.thing
        if isinstance(bot_action.action.thing, Creature):
            self.bot.active_creature = bot_action.action.thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)
        
        # Force swaps for fainted creatures
        self.handle_fainted_creatures()

    def execute_action(self, action: PlayerAction):
        if isinstance(action.action.thing, Creature):
            return # Swap already handled
            
        attacker = action.player
        defender = self.bot if attacker == self.player else self.player
        
        skill = action.action.thing
        damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def get_action_order(self, player_action: PlayerAction, bot_action: PlayerAction):
        if isinstance(player_action.action.thing, Creature) or isinstance(bot_action.action.thing, Creature):
            return (player_action, bot_action) # Swaps always go first
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (player_action, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return (bot_action, player_action)
        else:
            return (player_action, bot_action) if random.random() < 0.5 else (bot_action, player_action)

    def handle_fainted_creatures(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available = self.get_available_creatures(player)
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You win!" if player_alive else "You lose!"
            self._show_text(self.player, winner)
            return True
            
        return False
