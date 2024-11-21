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
        try:
            while True:
                # Player turn
                player_action = self.get_player_action(self.player)
                opponent_action = self.get_player_action(self.opponent)
                
                # Execute actions
                self.resolve_turn(player_action, opponent_action)
                
                # Check for battle end
                if self.check_battle_end():
                    break
        finally:
            # Reset creature states before leaving scene
            self.reset_creatures(self.player)
            self.reset_creatures(self.opponent)

    def reset_creatures(self, player):
        for creature in player.creatures:
            creature.hp = creature.max_hp
        player.active_creature = None

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if opponent_action[0] == "attack":
            actions.append((self.opponent, opponent_action[1]))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, skill in actions:
            defender = self.opponent if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)

    def execute_skill(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}")

        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing

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
