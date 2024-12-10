from typing import List, Optional, Tuple
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        # Initialize creatures
        for p in [self.player, self.opponent]:
            p.active_creature = p.creatures[0]
            # Store initial HP values
            for creature in p.creatures:
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

    def run(self):
        try:
            while True:
                if self._check_battle_end():
                    return
                    
                player_action = self._handle_turn_choices(self.player)
                opponent_action = self._handle_turn_choices(self.opponent)
                
                self._resolve_actions(player_action, opponent_action)
        finally:
            # Reset creature states when leaving scene
            self._reset_creatures_state()

    def _reset_creatures_state(self):
        for p in [self.player, self.opponent]:
            for creature in p.creatures:
                creature.hp = creature.max_hp
            p.active_creature = p.creatures[0]

    def _handle_turn_choices(self, current_player: Player) -> Tuple[str, Optional[Skill], Optional[Creature]]:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_result = self._handle_skill_choice(current_player)
                if skill_result:
                    return ("attack", skill_result, None)
            else:
                creature_result = self._handle_swap_choice(current_player)
                if creature_result:
                    return ("swap", None, creature_result)

    def _handle_skill_choice(self, current_player: Player) -> Optional[Skill]:
        back_button = Button("Back")
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        skill_choices.append(back_button)
        
        choice = self._wait_for_choice(current_player, skill_choices)
        if choice == back_button:
            return None
        return choice.thing

    def _handle_swap_choice(self, current_player: Player) -> Optional[Creature]:
        available_creatures = [c for c in current_player.creatures 
                            if c.hp > 0 and c != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap!")
            return None
            
        back_button = Button("Back")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        creature_choices.append(back_button)
        
        choice = self._wait_for_choice(current_player, creature_choices)
        if choice == back_button:
            return None
        return choice.thing

    def _resolve_actions(self, player_action: Tuple, opponent_action: Tuple):
        # Handle swaps first
        for action, player in [(player_action, self.player), (opponent_action, self.opponent)]:
            if action[0] == "swap":
                player.active_creature = action[2]
                self._show_text(self.player, f"{player.display_name} swapped to {action[2].display_name}!")

        # Then handle attacks
        actions = [(player_action, self.player, self.opponent), 
                  (opponent_action, self.opponent, self.player)]
        
        # Sort by speed with random tiebreaker
        actions.sort(key=lambda x: (x[1].active_creature.speed, random.random()), reverse=True)
        
        for action, attacker, defender in actions:
            if action[0] == "attack":
                skill = action[1]
                damage = self._calculate_damage(skill, attacker.active_creature, defender.active_creature)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")

                if defender.active_creature.hp == 0:
                    self._handle_knockout(defender)

    def _calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, player: Player):
        self._show_text(self.player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            winner = self.opponent if player == self.player else self.player
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")

    def _check_battle_end(self) -> bool:
        for player in [self.player, self.opponent]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False
