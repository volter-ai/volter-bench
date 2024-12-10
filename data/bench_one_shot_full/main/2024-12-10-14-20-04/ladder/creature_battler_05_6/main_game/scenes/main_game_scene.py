from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
> Swap (if available)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Execute actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures_state()
                self._quit_whole_game()

    def reset_creatures_state(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def get_player_action(self, player):
        # First check if we need to force a swap due to knocked out active creature
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if not valid_creatures:
                # No valid creatures left - battle should end
                return None
            choices = [SelectThing(creature) for creature in valid_creatures]
            return ("swap", self._wait_for_choice(player, choices).thing)

        while True:  # Main choice loop
            # Normal turn choices
            choices = [Button("Attack")]
            # Only add swap if there are valid creatures to swap to
            valid_swap_targets = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if valid_swap_targets:
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                attack_result = self.get_attack_choice(player)
                if attack_result:  # None means "Back" was chosen
                    return attack_result
            elif choice.display_name == "Swap":
                swap_result = self.get_swap_choice(player)
                if swap_result:  # None means "Back" was chosen
                    return swap_result

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Back":
            return None
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        choices = [SelectThing(creature) for creature in valid_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Back":
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle case where a player has no valid actions
        if player_action is None or opponent_action is None:
            return
            
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort by action type (swaps first) then by speed with random tiebreaker
        def sort_key(action_tuple):
            player, (action_type, thing) = action_tuple
            is_swap = action_type == "swap"
            speed = player.active_creature.speed
            # Add random tiebreaker that's consistent within this turn
            tiebreaker = random.random()
            return (not is_swap, -speed, tiebreaker)
            
        actions.sort(key=sort_key)
        
        for player, action in actions:
            action_type, thing = action
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(player, f"{player.display_name} swapped to {thing.display_name}!")
            else:
                self.execute_attack(player, thing)
                
            if self.check_battle_end():
                return

    def execute_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
                
        return False
