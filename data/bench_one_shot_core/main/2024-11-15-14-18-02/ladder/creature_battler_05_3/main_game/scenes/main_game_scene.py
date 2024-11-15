from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize player creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        
        # Initialize opponent creatures
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap
"""

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = None
        
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self.opponent.active_creature = None

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                return

            # Resolve actions
            self.resolve_actions(player_action, opponent_action)

            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player):
        if not self.handle_fainted_creature(player):
            return None
            
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])

        if choice == attack:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button):
            return self.get_player_action(player)
        return ("attack", choice.thing)

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button):
            return self.get_player_action(player)
        return ("swap", choice.thing)

    def handle_fainted_creature(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return False
                
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        return True

    def resolve_actions(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]

        # Then handle attacks
        first_action, second_action = self.determine_order(player_action, opponent_action)
        
        # Execute first action
        if first_action == player_action:
            self.execute_action(first_action, self.player, self.opponent)
        else:
            self.execute_action(first_action, self.opponent, self.player)
            
        # Execute second action
        if second_action == player_action:
            self.execute_action(second_action, self.player, self.opponent)
        else:
            self.execute_action(second_action, self.opponent, self.player)

    def determine_order(self, player_action, opponent_action):
        if player_action[0] == "swap" or opponent_action[0] == "swap":
            return (player_action, opponent_action)
            
        p_speed = self.player.active_creature.speed
        o_speed = self.opponent.active_creature.speed
        
        if p_speed > o_speed or (p_speed == o_speed and random.random() < 0.5):
            return (player_action, opponent_action)
        return (opponent_action, player_action)

    def execute_action(self, action, attacker, defender):
        if action[0] == "attack":
            skill = action[1]
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp -= damage
            
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * factor)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness.get((skill_type, defender_type), 1.0)

    def check_battle_end(self):
        p_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        o_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)

        if not p_has_creatures or not o_has_creatures:
            winner = "You" if p_has_creatures else "Opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            # Reset creatures before transitioning
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
