from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Reset creatures
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

Your choices:
> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self._quit_whole_game()
                return
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                self._quit_whole_game()
                return
                
            # Resolution phase
            self.resolve_actions(
                (self.player, player_action),
                (self.opponent, opponent_action)
            )
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def get_player_action(self, player):
        if not self.handle_knockouts(player):
            return None
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_knockouts(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                winner = self.player if player == self.opponent else self.opponent
                self._show_text(self.player, f"{winner.display_name} wins!")
                return False
                
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def handle_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
            
        return ("attack", choice.thing)

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return self.get_player_action(player)
            
        choices = [SelectThing(c) for c in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
            
        return ("swap", choice.thing)

    def resolve_actions(self, player_action_tuple, opponent_action_tuple):
        # Handle swaps first
        player, player_action = player_action_tuple
        opponent, opponent_action = opponent_action_tuple
        
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            
        # Then handle attacks
        first, second = self.get_action_order(player_action_tuple, opponent_action_tuple)
        self.execute_action(*first)
        self.execute_action(*second)

    def get_action_order(self, player_action_tuple, opponent_action_tuple):
        player, player_action = player_action_tuple
        opponent, opponent_action = opponent_action_tuple
        
        if player_action[0] == "swap" or opponent_action[0] == "swap":
            return player_action_tuple, opponent_action_tuple
            
        p_speed = self.player.active_creature.speed
        o_speed = self.opponent.active_creature.speed
        
        if p_speed > o_speed or (p_speed == o_speed and random.random() < 0.5):
            return player_action_tuple, opponent_action_tuple
        return opponent_action_tuple, player_action_tuple

    def execute_action(self, acting_player, action):
        if action[0] != "attack":
            return
            
        skill = action[1]
        attacker = acting_player
        defender = self.opponent if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

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
        p_creatures_alive = any(c.hp > 0 for c in self.player.creatures)
        o_creatures_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not p_creatures_alive or not o_creatures_alive:
            winner = self.player if p_creatures_alive else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
        return False
