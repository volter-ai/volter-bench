from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap
"""

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

    def run(self):
        try:
            while True:
                # Player turn
                player_action = self.get_player_action(self.player)
                bot_action = self.get_player_action(self.bot)
                
                # Resolve actions
                self.resolve_turn(player_action, bot_action)
                
                # Check for battle end
                if self.check_battle_end():
                    self.reset_creatures()
                    self._quit_whole_game()
                    break
        except:
            # Ensure creatures are reset even if an exception occurs
            self.reset_creatures()
            raise

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skills.append(back_button)
                skill_choice = self._wait_for_choice(player, skills)
                
                # Check if it's the back button
                if isinstance(skill_choice, Button):
                    continue
                    
                return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                back_button = Button("Back")
                available_creatures.append(back_button)
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                # Check if it's the back button
                if isinstance(swap_choice, Button):
                    continue
                    
                return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, action[1])
                
                # Force swap if creature fainted
                if defender.active_creature.hp <= 0:
                    available = [c for c in defender.creatures if c.hp > 0]
                    if available:
                        choices = [SelectThing(c) for c in available]
                        swap_choice = self._wait_for_choice(defender, choices)
                        defender.active_creature = swap_choice.thing

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
