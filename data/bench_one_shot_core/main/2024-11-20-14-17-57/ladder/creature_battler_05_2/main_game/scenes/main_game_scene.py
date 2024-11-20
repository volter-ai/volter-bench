from typing import List, Dict, Tuple
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        """Reset all creatures to starting state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate base damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def _handle_knockouts(self, player: Player) -> bool:
        """Returns True if player can continue, False if they're out of creatures"""
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
                
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _execute_turn(self, first_player: Player, second_player: Player, 
                     first_action: Tuple[str, Skill | Creature], 
                     second_action: Tuple[str, Skill | Creature]):
        for current_player, other_player, (action_type, action) in [
            (first_player, second_player, first_action),
            (second_player, first_player, second_action)
        ]:
            if current_player.active_creature.hp <= 0:
                continue
                
            if action_type == "attack":
                damage = self._calculate_damage(
                    current_player.active_creature,
                    other_player.active_creature,
                    action
                )
                other_player.active_creature.hp -= damage
                self._show_text(current_player, 
                    f"{current_player.active_creature.display_name} used {action.display_name}!")
                self._show_text(other_player,
                    f"{current_player.active_creature.display_name} used {action.display_name}!")
            else:  # swap
                current_player.active_creature = action
                self._show_text(current_player,
                    f"Switched to {action.display_name}!")
                self._show_text(other_player,
                    f"Opponent switched to {action.display_name}!")

    def _get_player_action(self, player: Player) -> Tuple[str, Skill | Creature]:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if isinstance(skill_choice, SelectThing):
                    return "attack", skill_choice.thing
                    
            else:  # Swap
                available = self._get_available_creatures(player)
                if available:
                    creature_choices = [SelectThing(c) for c in available]
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    
                    if isinstance(creature_choice, SelectThing):
                        return "swap", creature_choice.thing

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Get actions
            player_action = self._get_player_action(self.player)
            opponent_action = self._get_player_action(self.opponent)
            
            # Determine order
            if (player_action[0] == "swap" and opponent_action[0] != "swap") or \
               (player_action[0] != "swap" and opponent_action[0] == "swap"):
                # Swaps go first
                first = (self.player, player_action) if player_action[0] == "swap" else (self.opponent, opponent_action)
                second = (self.opponent, opponent_action) if player_action[0] == "swap" else (self.player, player_action)
            else:
                # Speed determines order
                if self.player.active_creature.speed > self.opponent.active_creature.speed:
                    first = (self.player, player_action)
                    second = (self.opponent, opponent_action)
                else:
                    first = (self.opponent, opponent_action)
                    second = (self.player, player_action)
            
            # Execute turn
            self._execute_turn(first[0], second[0], first[1], second[1])
            
            # Handle knockouts
            player_can_continue = self._handle_knockouts(self.player)
            opponent_can_continue = self._handle_knockouts(self.opponent)
            
            if not player_can_continue:
                self._show_text(self.player, "You lost!")
                self._show_text(self.opponent, "You won!")
                break
            elif not opponent_can_continue:
                self._show_text(self.player, "You won!")
                self._show_text(self.opponent, "You lost!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
