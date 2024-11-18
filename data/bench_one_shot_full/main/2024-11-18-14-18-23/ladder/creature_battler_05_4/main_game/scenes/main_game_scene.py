from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None
            
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
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

    def resolve_turn(self, player_action, bot_action):
        actions = [
            (self.player, player_action),
            (self.bot, bot_action)
        ]
        
        # Handle swaps first
        for player, (action_type, target) in actions:
            if action_type == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")

        # Then handle attacks
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)
            
        for attacker, (action_type, skill) in actions:
            if action_type == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, skill)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(
            skill.skill_type,
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * effectiveness)
        defender.active_creature.hp -= final_damage
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )
        
        if defender.active_creature.hp <= 0:
            defender.active_creature.hp = 0
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            
            # Force swap if possible
            available_creatures = [
                c for c in defender.creatures if c.hp > 0 and c != defender.active_creature
            ]
            
            if available_creatures:
                choices = [SelectThing(c) for c in available_creatures]
                choice = self._wait_for_choice(defender, choices)
                defender.active_creature = choice.thing
                self._show_text(defender, f"Go! {choice.thing.display_name}!")

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
                self._show_text(self.player, 
                    f"{winner.display_name} wins! All of {player.display_name}'s creatures are knocked out!"
                )
                return True
        return False
