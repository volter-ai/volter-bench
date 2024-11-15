from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Dict

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Track current HP for all creatures
        self.current_hp: Dict[str, int] = {}
        # Initialize HP for player creatures
        for creature in self.player.creatures:
            self.current_hp[creature.uid] = creature.hp
        # Initialize HP for bot creatures
        for creature in self.bot.creatures:
            self.current_hp[creature.uid] = creature.hp
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name if p_creature else 'No Creature'}: {self.current_hp.get(p_creature.uid, 0) if p_creature else 0}/{p_creature.hp if p_creature else 0} HP
Foe's {b_creature.display_name if b_creature else 'No Creature'}: {self.current_hp.get(b_creature.uid, 0) if b_creature else 0}/{b_creature.hp if b_creature else 0} HP
"""

    def reset_scene_state(self):
        """Reset all battle-related state"""
        # Reset active creatures
        self.player.active_creature = None
        self.bot.active_creature = None
        # Clear current HP tracking
        self.current_hp.clear()

    def run(self):
        try:
            while True:
                # Player turn
                player_action = self.get_turn_action(self.player)
                bot_action = self.get_turn_action(self.bot)
                
                # Resolve actions
                self.resolve_turn(player_action, bot_action)
                
                # Check for battle end
                if self.check_battle_end():
                    break
        finally:
            # Always reset state when leaving the scene
            self.reset_scene_state()
            self._quit_whole_game()

    def get_turn_action(self, player):
        if self.current_hp[player.active_creature.uid] <= 0:
            return self.force_swap(player)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.choose_attack(player)
        else:
            return self.choose_swap(player)

    def choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_turn_action(player)
        return ("attack", choice.thing)

    def choose_swap(self, player):
        available = [c for c in player.creatures if c != player.active_creature and self.current_hp[c.uid] > 0]
        choices = [SelectThing(creature) for creature in available]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_turn_action(player)
        return ("swap", choice.thing)

    def force_swap(self, player):
        available = [c for c in player.creatures if self.current_hp[c.uid] > 0]
        if not available:
            return None
        
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return

        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            first, second = self.determine_order(
                (self.player, player_action[1]),
                (self.bot, bot_action[1])
            )
            self.execute_attack(first[0], first[1], second[0].active_creature)
            if self.current_hp[second[0].active_creature.uid] > 0:
                self.execute_attack(second[0], second[1], first[0].active_creature)

    def determine_order(self, player_data, bot_data):
        p_speed = player_data[0].active_creature.speed
        b_speed = bot_data[0].active_creature.speed
        
        if p_speed > b_speed:
            return player_data, bot_data
        elif b_speed > p_speed:
            return bot_data, player_data
        else:
            if random.random() < 0.5:
                return player_data, bot_data
            return bot_data, player_data

    def execute_attack(self, attacker, skill, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        
        # Update HP in our state dictionary
        self.current_hp[defender.uid] = max(0, self.current_hp[defender.uid] - final_damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {final_damage} damage!")

    def check_battle_end(self):
        player_has_creatures = any(self.current_hp[c.uid] > 0 for c in self.player.creatures)
        bot_has_creatures = any(self.current_hp[c.uid] > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
