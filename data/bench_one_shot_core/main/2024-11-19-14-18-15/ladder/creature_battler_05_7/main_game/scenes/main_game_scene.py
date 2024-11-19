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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Execute actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature HP before transitioning
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.opponent.creatures:
                    creature.hp = creature.max_hp
                    
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def has_valid_swaps(self, player):
        return any(c for c in player.creatures 
                  if c != player.active_creature and c.hp > 0)

    def get_player_action(self, player):
        # If no valid swaps available, force attack
        if not self.has_valid_swaps(player):
            return self.get_attack_choice(player)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        # Create skill choices plus back button
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            # Recursively get new action if player goes back
            return self.get_player_action(player)
        else:
            return ("attack", choice.thing)

    def get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        
        # This should never happen now due to has_valid_swaps check
        assert len(available_creatures) > 0, "No valid creatures to swap to"
        
        # Create creature choices plus back button
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            # Recursively get new action if player goes back
            return self.get_player_action(player)
        else:
            return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]

        # Then handle attacks based on speed
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                self.execute_attack(self.player, player_action[1], self.opponent)
                self.execute_attack(self.opponent, opponent_action[1], self.player)
            else:
                self.execute_attack(self.opponent, opponent_action[1], self.player)
                self.execute_attack(self.player, player_action[1], self.opponent)

    def execute_attack(self, attacker, skill, defender):
        if defender.active_creature.hp <= 0:
            return

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

        if defender.active_creature.hp <= 0:
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing
        
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
