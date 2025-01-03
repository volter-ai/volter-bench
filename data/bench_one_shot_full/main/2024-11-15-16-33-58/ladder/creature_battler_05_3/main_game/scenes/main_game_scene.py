from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap (if available)
> Back (when in submenu)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Return to main menu after showing result
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            
            # Only add swap option if there are valid creatures to swap to
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
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
            else:  # Swap
                # Show creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main choices
                return choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
            
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            self._show_text(self.player, f"Opponent switched to {opponent_action.thing.display_name}!")

        # Then handle attacks
        first = self.player
        second = self.opponent
        first_action = player_action
        second_action = opponent_action

        if isinstance(first_action.thing, Skill) and isinstance(second_action.thing, Skill):
            if self.opponent.active_creature.speed > self.player.active_creature.speed:
                first, second = second, first
                first_action, second_action = second_action, first_action
            elif self.opponent.active_creature.speed == self.player.active_creature.speed:
                if random.random() < 0.5:
                    first, second = second, first
                    first_action, second_action = second_action, first_action

        if isinstance(first_action.thing, Skill):
            self.execute_attack(first, second, first_action.thing)
        if isinstance(second_action.thing, Skill) and second.active_creature.hp > 0:
            self.execute_attack(second, first, second_action.thing)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            
            # Check if player has any creatures left before trying to swap
            available_creatures = [c for c in defender.creatures if c.hp > 0]
            if available_creatures:
                new_creature = self._wait_for_choice(defender,
                    [SelectThing(c) for c in available_creatures]).thing
                defender.active_creature = new_creature
                self._show_text(self.player, 
                    f"{'You' if defender == self.player else 'Opponent'} sent out {new_creature.display_name}!")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

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
