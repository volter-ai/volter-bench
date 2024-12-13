from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from itertools import groupby
from operator import itemgetter

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return ("attack", skill_choice.thing)

            else: # Swap
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                if isinstance(swap_choice, Button):
                    continue
                    
                return ("swap", swap_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1]))

        # Sort actions by speed and randomize ties
        if actions:
            # Group actions by speed
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            speed_groups = []
            for speed, group in groupby(actions, key=lambda x: x[0].active_creature.speed):
                group_list = list(group)
                random.shuffle(group_list)  # Randomize order within same speed
                speed_groups.extend(group_list)
            
            # Execute actions in order
            for attacker, defender, skill in speed_groups:
                self.execute_skill(attacker, defender, skill)
                
                if defender.active_creature.hp <= 0:
                    self.handle_knockout(defender)
                    if self.check_battle_end():
                        return

    def execute_skill(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense * 
                         skill.base_damage)

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp -= final_damage

        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}! "
                       f"Dealt {final_damage} damage!")

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
        self._show_text(self.player, 
                       f"{player.active_creature.display_name} was knocked out!")
        
        available = [c for c in player.creatures if c.hp > 0]
        
        if available:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(self.player,
                          f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        p_available = any(c.hp > 0 for c in self.player.creatures)
        b_available = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_available or not b_available:
            # Reset all creatures before transitioning
            for creature in self.player.creatures:
                creature.hp = creature.max_hp
            for creature in self.bot.creatures:
                creature.hp = creature.max_hp
                
            if not p_available:
                self._show_text(self.player, "You lost the battle!")
            else:
                self._show_text(self.player, "You won the battle!")
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
