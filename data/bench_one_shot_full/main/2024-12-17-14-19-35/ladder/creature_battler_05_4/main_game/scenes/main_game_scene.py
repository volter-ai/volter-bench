from typing import List, Optional, Tuple
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player: Player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        # Reset creature HPs
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn_choice(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self._handle_turn_choice(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self._resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _handle_turn_choice(self, current_player: Player) -> Optional[Tuple[str, Skill | Creature]]:
        while True:  # Main choice loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                skill_choices = [
                    SelectThing(skill, label=f"{skill.display_name} ({skill.base_damage} dmg)")
                    for skill in current_player.active_creature.skills
                ]
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                
                if skill_choice == back_button:
                    continue  # Go back to main choice
                    
                return ("attack", skill_choice.thing)
                
            else:  # Swap choice
                # Show available creatures with Back option
                back_button = Button("Back")
                available_creatures = [
                    SelectThing(creature)
                    for creature in current_player.creatures
                    if creature.hp > 0 and creature != current_player.active_creature
                ]
                
                if not available_creatures:
                    return None
                    
                available_creatures.append(back_button)
                creature_choice = self._wait_for_choice(current_player, available_creatures)
                
                if creature_choice == back_button:
                    continue  # Go back to main choice
                    
                return ("swap", creature_choice.thing)

    def _resolve_turn(self, player_action: Tuple[str, Skill | Creature], opponent_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            self._show_text(self.player, f"Foe sends out {opponent_action[1].display_name}!")

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if opponent_action[0] == "attack":
            actions.append((self.opponent, opponent_action[1]))
            
        # Sort by speed, using random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        # Execute attacks
        for attacker, skill in actions:
            defender = self.opponent if attacker == self.player else self.player
            self._execute_attack(attacker, defender, skill)

    def _execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + skill.base_damage 
                         - defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * attacker.active_creature.sp_attack 
                         / defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, 
                                             defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show attack message
        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")

    def _get_type_multiplier(self, attack_type: str, defender_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self) -> bool:
        # Check if either player has all creatures knocked out
        player_has_active = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_active = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_active:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_active:
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is knocked out
        if self.player.active_creature.hp <= 0:
            available = [
                SelectThing(c) for c in self.player.creatures 
                if c.hp > 0
            ]
            if available:
                self._show_text(self.player, f"{self.player.active_creature.display_name} fainted!")
                choice = self._wait_for_choice(self.player, available)
                self.player.active_creature = choice.thing
                
        if self.opponent.active_creature.hp <= 0:
            available = [c for c in self.opponent.creatures if c.hp > 0]
            if available:
                self._show_text(self.player, f"Foe's {self.opponent.active_creature.display_name} fainted!")
                self.opponent.active_creature = available[0]
                
        return False
