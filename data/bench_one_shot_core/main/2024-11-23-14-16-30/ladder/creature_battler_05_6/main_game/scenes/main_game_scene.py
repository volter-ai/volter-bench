from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
{self.opponent.display_name}'s {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

{self.player.display_name}'s {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal" or defend_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def _handle_player_turn(self, player, is_forced_swap=False):
        if is_forced_swap:
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            choices = [SelectThing(creature) for creature in available_creatures]
            if not choices:
                return None
            choice = self._wait_for_choice(player, choices)
            return ("swap", choice.thing)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            back_button = Button("Back")
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            
            skill_choice = self._wait_for_choice(player, skill_choices)
            if skill_choice == back_button:
                return self._handle_player_turn(player)
            return ("attack", skill_choice.thing)
            
        else:
            back_button = Button("Back")
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            choices = [SelectThing(creature) for creature in available_creatures]
            choices.append(back_button)
            
            swap_choice = self._wait_for_choice(player, choices)
            if swap_choice == back_button:
                return self._handle_player_turn(player)
            return ("swap", swap_choice.thing)

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_turn(self.player)
            if not player_action:
                self._show_text(self.player, "You have no more creatures! You lose!")
                self._quit_whole_game()
                
            # Opponent turn
            opponent_action = self._handle_player_turn(self.opponent)
            if not opponent_action:
                self._show_text(self.player, "Opponent has no more creatures! You win!")
                self._quit_whole_game()

            # Resolve actions
            actions = [
                (self.player, player_action),
                (self.opponent, opponent_action)
            ]
            
            # Sort by speed for attacks
            if all(action[1][0] == "attack" for action in actions):
                actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
                if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                    random.shuffle(actions)
                    
            # Execute actions
            for player, (action_type, action_target) in actions:
                opponent = self.opponent if player == self.player else self.player
                
                if action_type == "swap":
                    player.active_creature = action_target
                    self._show_text(self.player, f"{player.display_name} swapped to {action_target.display_name}!")
                else:
                    damage = self._calculate_damage(player.active_creature, opponent.active_creature, action_target)
                    opponent.active_creature.hp -= damage
                    self._show_text(self.player, 
                        f"{player.display_name}'s {player.active_creature.display_name} used {action_target.display_name}! "
                        f"Dealt {damage} damage!")
                    
                    if opponent.active_creature.hp <= 0:
                        self._show_text(self.player, f"{opponent.active_creature.display_name} was knocked out!")
                        swap_action = self._handle_player_turn(opponent, is_forced_swap=True)
                        if not swap_action:
                            if opponent == self.player:
                                self._show_text(self.player, "You have no more creatures! You lose!")
                            else:
                                self._show_text(self.player, "Opponent has no more creatures! You win!")
                            self._quit_whole_game()
                        opponent.active_creature = swap_action[1]
                        self._show_text(self.player, f"{opponent.display_name} sent out {opponent.active_creature.display_name}!")
