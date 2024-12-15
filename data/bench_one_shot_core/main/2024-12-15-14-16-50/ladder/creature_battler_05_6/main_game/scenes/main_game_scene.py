from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.reset_creatures()
        
    def reset_creatures(self):
        # Reset all creatures to starting state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Phase: {'Player Choice' if self.current_phase == self.player_choice_phase else 'Foe Choice' if self.current_phase == self.foe_choice_phase else 'Resolution'}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.player_choice_phase()
            
            # Foe Choice Phase
            opponent_action = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature states before leaving
                self.reset_creatures()
                self._quit_whole_game()

    def player_choice_phase(self):
        while True:
            # Main choice menu
            choices = [
                Button("Attack"),
                Button("Swap")
            ]
            main_choice = self._wait_for_choice(self.player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                choices.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(self.player, choices)
                if skill_choice.display_name == "Back":
                    continue
                return skill_choice
                
            else:  # Swap
                # Swap submenu
                valid_creatures = [c for c in self.player.creatures if c.hp > 0 and c != self.player.active_creature]
                if not valid_creatures:
                    self._show_text(self.player, "No other creatures available to swap!")
                    continue
                    
                choices = [SelectThing(creature) for creature in valid_creatures]
                choices.append(Button("Back"))
                
                swap_choice = self._wait_for_choice(self.player, choices)
                if swap_choice.display_name == "Back":
                    continue
                return swap_choice

    def foe_choice_phase(self):
        # Bot uses same logic as player but without "Back" options
        valid_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
        choices = [Button("Attack")]
        if valid_creatures:
            choices.append(Button("Swap"))
            
        main_choice = self._wait_for_choice(self.opponent, choices)
        
        if main_choice.display_name == "Attack":
            return self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent.active_creature.skills])
        else:
            return self._wait_for_choice(self.opponent,
                [SelectThing(creature) for creature in valid_creatures])

    def resolution_phase(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            self.opponent.active_creature = opponent_action.thing

        # Determine action order based on speed
        first, second = self.get_action_order(player_action, opponent_action)
        
        # Execute actions in order
        self.execute_action(first)
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
            return  # Skip if it's a swap
            
        skill = action.thing
        attacker = self.player.active_creature if action in self.player.active_creature.skills else self.opponent.active_creature
        defender = self.opponent.active_creature if action in self.player.active_creature.skills else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        # Force swap if knocked out
        if defender.hp == 0:
            self.handle_knockout(self.player if defender in self.player.creatures else self.opponent)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            winner = self.player if player_alive else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
            
        return False
