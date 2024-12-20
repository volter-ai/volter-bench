from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self.has_available_swaps(self.player) else ""}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Store current turn's actions
            self.current_player_action = player_action
            self.current_opponent_action = opponent_action
            
            self.resolve_actions(player_action, opponent_action)
            
            # Clear turn actions
            self.current_player_action = None
            self.current_opponent_action = None
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature states before ending
                self.reset_creatures(self.player)
                self.reset_creatures(self.opponent)
                self._quit_whole_game()

    def reset_creatures(self, player):
        """Reset all creatures to their initial state"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def has_available_swaps(self, player):
        """Check if player has any creatures they can swap to"""
        return any(c != player.active_creature and c.hp > 0 for c in player.creatures)

    def get_player_action(self, player):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            if self.has_available_swaps(player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice
            else:
                # Show available creatures with Back option
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice

    def resolve_actions(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            self.opponent.active_creature = opponent_action.thing

        # Then handle attacks
        first, second = self.get_action_order(player_action, opponent_action)
        self.execute_action(first)
        
        # Only execute second action if creature still has HP
        if (first == player_action and self.opponent.active_creature.hp > 0) or \
           (first == opponent_action and self.player.active_creature.hp > 0):
            self.execute_action(second)

    def get_action_order(self, player_action, opponent_action):
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return player_action, opponent_action
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            return opponent_action, player_action
        else:
            return random.choice([(player_action, opponent_action), (opponent_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return  # Skip if it's a swap action
            
        skill = action.thing
        # Determine attacker/defender based on stored actions
        if action == self.current_player_action:
            attacker = self.player.active_creature
            defender = self.opponent.active_creature
        else:
            attacker = self.opponent.active_creature
            defender = self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
