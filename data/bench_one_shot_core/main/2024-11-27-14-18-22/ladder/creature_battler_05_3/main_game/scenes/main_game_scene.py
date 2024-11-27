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
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()
                self._quit_whole_game()

    def reset_creatures(self):
        # Reset player creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        
        # Reset opponent creatures
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def force_swap(self, player):
        """Force player to swap when their active creature is knocked out"""
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        
        if not available_creatures:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
        swap_choice = self._wait_for_choice(player,
            [SelectThing(creature) for creature in available_creatures])
        
        player.active_creature = swap_choice.thing
        return True

    def get_player_action(self, player):
        while True:
            # Main action menu
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Attack submenu
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(back_button)
                
                sub_choice = self._wait_for_choice(player, choices)
                if sub_choice == back_button:
                    continue
                return sub_choice
                
            else:  # Swap selected
                # Swap submenu
                available_creatures = [c for c in player.creatures 
                                     if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                
                back_button = Button("Back")
                choices = [SelectThing(creature) for creature in available_creatures]
                choices.append(back_button)
                
                sub_choice = self._wait_for_choice(player, choices)
                if sub_choice == back_button:
                    continue
                return sub_choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Then handle attacks
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort by speed and randomize equal speeds
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # If speeds are equal, randomize order
        if (len(actions) == 2 and 
            isinstance(actions[0][1].thing, Skill) and 
            isinstance(actions[1][1].thing, Skill) and
            actions[0][0].active_creature.speed == actions[1][0].active_creature.speed):
            random.shuffle(actions)
        
        # Execute actions
        for actor, action in actions:
            if isinstance(action.thing, Skill):
                self.execute_skill(actor, action.thing)
                
                # Check if defender needs to swap
                defender = self.opponent if actor == self.player else self.player
                if defender.active_creature.hp <= 0:
                    if not self.force_swap(defender):
                        # No available creatures to swap to, battle will end
                        return

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, 
            defender.active_creature.hp - final_damage)

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
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost!")
            return True
        elif not has_available_creatures(self.opponent):
            self._show_text(self.player, "You won!")
            return True
            
        return False
