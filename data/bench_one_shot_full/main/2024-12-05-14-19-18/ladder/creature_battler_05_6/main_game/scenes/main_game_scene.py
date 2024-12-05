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

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature HP before leaving scene
                self.reset_creatures(self.player)
                self.reset_creatures(self.opponent)
                # Transition back to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def reset_creatures(self, player):
        """Reset all creatures' HP to their max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            self._show_text(self.opponent, f"Opponent sends out {opponent_action[1].display_name}!")

        # Handle attacks in speed order
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            first = self.player if self.player.active_creature.speed >= self.opponent.active_creature.speed else self.opponent
            second = self.opponent if first == self.player else self.player
            first_action = player_action if first == self.player else opponent_action
            second_action = opponent_action if first == self.player else player_action
            
            self.execute_attack(first, second, first_action[1])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if multiplier > 1:
            self._show_text(attacker, "It's super effective!")
        elif multiplier < 1:
            self._show_text(attacker, "It's not very effective...")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
            
        if not has_available_creatures(self.opponent):
            self._show_text(self.player, "You won the battle!")
            return True
            
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                choice = self._wait_for_choice(self.player, [SelectThing(c) for c in available])
                self.player.active_creature = choice.thing
                
        if self.opponent.active_creature.hp <= 0:
            available = [c for c in self.opponent.creatures if c.hp > 0]
            if available:
                choice = self._wait_for_choice(self.opponent, [SelectThing(c) for c in available])
                self.opponent.active_creature = choice.thing
                
        return False
