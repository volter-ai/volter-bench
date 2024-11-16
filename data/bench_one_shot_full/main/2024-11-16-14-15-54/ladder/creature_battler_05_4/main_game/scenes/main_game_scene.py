from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def reset_creature_states(self):
        """Reset all creatures to their initial state"""
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def run(self):
        while True:
            # Check for battle end before each turn
            if self.check_battle_end():
                self.reset_creature_states()  # Reset before quitting
                self._quit_whole_game()
                return
                
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:  # No valid actions possible
                self.reset_creature_states()  # Reset before quitting
                self._quit_whole_game()
                return
                
            bot_action = self.get_player_action(self.bot)
            if not bot_action:  # No valid actions possible
                self.reset_creature_states()  # Reset before quitting
                self._quit_whole_game()
                return
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        # If active creature is fainted, must swap if possible
        if player.active_creature.hp <= 0:
            available = [c for c in player.creatures if c.hp > 0]
            if not available:
                return None
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return choice
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            available_creatures = self.get_available_creatures(player)
            if not available_creatures:  # If no creatures to swap to, force attack
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                return self._wait_for_choice(player, skill_choices)
            
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed for skill execution
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
            else:
                self.execute_skill(player, action.thing)

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

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
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
