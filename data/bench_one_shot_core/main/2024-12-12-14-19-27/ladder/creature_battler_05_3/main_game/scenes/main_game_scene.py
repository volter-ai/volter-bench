from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Tuple, Optional

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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game instead of breaking
                
            # Check if either active creature is knocked out
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()
            if self.bot.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()
                    
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def handle_forced_swap(self, player) -> bool:
        """Returns True if swap successful, False if no valid creatures left"""
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return False
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self.get_player_action(player)
            return choice
        else:
            valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not valid_creatures:
                self._show_text(player, "No other creatures available to swap to!")
                return self.get_player_action(player)
                
            choices = [SelectThing(creature) for creature in valid_creatures]
            back_button = Button("Back")
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self.get_player_action(player)
            return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        first_owner = self.player if first_action == player_action else self.bot
        second_owner = self.player if second_action == player_action else self.bot
        
        self.execute_action(first_action, first_owner)
        if second_owner.active_creature.hp > 0:  # Only do second action if target still alive
            self.execute_action(second_action, second_owner)

    def get_action_order(self, player_action, bot_action) -> Tuple[SelectThing, SelectThing]:
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action: SelectThing, action_owner):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return  # Skip if it was a swap
            
        skill = action.thing
        attacker = action_owner.active_creature
        defender = self.bot.active_creature if action_owner == self.player else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_healthy = any(c.hp > 0 for c in self.player.creatures)
        bot_has_healthy = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_healthy:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_healthy:
            self._show_text(self.player, "You won!")
            return True
            
        return False
