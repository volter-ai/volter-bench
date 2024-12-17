from typing import List, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" + (" (Active)" if c == self.player.active_creature else "")
            for c in self.player.creatures
        )
        opponent_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" + (" (Active)" if c == self.opponent.active_creature else "")
            for c in self.opponent.creatures
        )
        
        return f"""=== Battle ===
Your Team:
{player_creatures_status}

Opponent's Team:
{opponent_creatures_status}

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_turn(self.player)
            if not player_action:
                return
                
            # Opponent turn
            opponent_action = self._handle_player_turn(self.opponent)
            if not opponent_action:
                return
                
            # Resolution phase
            self._resolve_actions(player_action, opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_player_turn(self, current_player: Player) -> Optional[dict]:
        if self._check_and_handle_ko(current_player):
            return None
            
        # Main choice
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            skill_choice = self._wait_for_choice(current_player, skill_choices)
            return {"type": "attack", "skill": skill_choice.thing}
            
        else:  # Swap
            # Show available creatures
            available_creatures = [
                c for c in current_player.creatures 
                if c != current_player.active_creature and c.hp > 0
            ]
            if not available_creatures:
                self._show_text(current_player, "No other creatures available!")
                return self._handle_player_turn(current_player)
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choice = self._wait_for_choice(current_player, creature_choices)
            return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_actions(self, player_action: dict, opponent_action: dict):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go, {self.player.active_creature.display_name}!")
            
        if opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]
            self._show_text(self.player, f"Opponent sends out {self.opponent.active_creature.display_name}!")

        # Then handle attacks
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort by speed for attack order
        if player_action["type"] == "attack" and opponent_action["type"] == "attack":
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                random.shuffle(actions)

        # Execute attacks
        for attacker, action in actions:
            if action["type"] == "attack":
                defender = self.opponent if attacker == self.player else self.player
                self._execute_attack(attacker, defender, action["skill"])

    def _execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + skill.base_damage 
                         - defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * attacker.active_creature.sp_attack 
                         / defender.active_creature.sp_defense)

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_and_handle_ko(self, player: Player) -> bool:
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                winner = "You" if player == self.opponent else "Opponent"
                self._show_text(self.player, f"{winner} won the battle!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return True
                
            self._show_text(self.player, 
                f"{player.active_creature.display_name} was knocked out!")
            creature_choices = [SelectThing(c) for c in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"Go, {new_creature.display_name}!")
        return False

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures or not opponent_has_creatures:
            winner = "You" if player_has_creatures else "Opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        """Reset all creatures to their original state when leaving the scene"""
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
