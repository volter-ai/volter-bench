from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class Action:
    actor: Creature
    target: Creature
    skill: Optional[Skill] = None
    is_swap: bool = False

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self._reset_creatures()
        self.battle_ended = False

    def _is_knocked_out(self, creature: Creature) -> bool:
        return creature.hp <= 0

    def _get_available_swap_creatures(self, player) -> list[Creature]:
        return [c for c in player.creatures 
                if not self._is_knocked_out(c) and c != player.active_creature]

    def _reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
{self.opponent.display_name}'s {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

{self.player.display_name}'s {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP

What will {p_creature.display_name} do?
> Attack
> Swap (if available)"""

    def run(self):
        while not self.battle_ended:
            # Player turn
            player_action = self._get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self._get_player_action(self.opponent)
            if not opponent_action:
                continue

            # Resolve actions
            self._resolve_actions(player_action, opponent_action)

            # Check for battle end
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

        # This should never be reached due to the transition above,
        # but adding as a safeguard
        self._transition_to_scene("MainMenuScene")

    def _get_player_action(self, player) -> Optional[Action]:
        if self._is_knocked_out(player.active_creature):
            if not self._handle_knocked_out(player):
                self.battle_ended = True
                return None
        
        choices = [Button("Attack")]
        if self._get_available_swap_creatures(player):
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_knocked_out(self, player) -> bool:
        available_creatures = [c for c in player.creatures if not self._is_knocked_out(c)]
        if not available_creatures:
            winner = self.player if player == self.opponent else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            return False
            
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _handle_attack_choice(self, player) -> Action:
        opponent = self.opponent if player == self.player else self.player
        choices = [SelectThing(s) for s in player.active_creature.skills]
        skill = self._wait_for_choice(player, choices).thing
        return Action(player.active_creature, opponent.active_creature, skill=skill)

    def _handle_swap_choice(self, player) -> Action:
        available_creatures = self._get_available_swap_creatures(player)
        choices = [SelectThing(c) for c in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        return Action(player.active_creature, new_creature, is_swap=True)

    def _resolve_actions(self, player_action: Action, opponent_action: Action):
        # Handle swaps first
        if player_action.is_swap:
            self.player.active_creature = player_action.target
        if opponent_action.is_swap:
            self.opponent.active_creature = opponent_action.target
            
        if not player_action.is_swap and not opponent_action.is_swap:
            # Determine order based on speed
            first = player_action
            second = opponent_action
            if opponent_action.actor.speed > player_action.actor.speed or \
               (opponent_action.actor.speed == player_action.actor.speed and random.random() < 0.5):
                first, second = second, first
                
            self._execute_skill(first)
            if not self._is_knocked_out(second.target):
                self._execute_skill(second)

    def _execute_skill(self, action: Action):
        if action.is_swap:
            return
            
        # Calculate damage
        if action.skill.is_physical:
            raw_damage = action.actor.attack + action.skill.base_damage - action.target.defense
        else:
            raw_damage = (action.actor.sp_attack / action.target.sp_defense) * action.skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(action.skill.skill_type, action.target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        action.target.hp = max(0, action.target.hp - final_damage)
        
        self._show_text(self.player, 
            f"{action.actor.display_name} used {action.skill.display_name} on {action.target.display_name}!")

    def _get_type_multiplier(self, skill_type: str, target_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def _check_battle_end(self) -> bool:
        return any(all(self._is_knocked_out(c) for c in p.creatures) 
                  for p in [self.player, self.opponent])
