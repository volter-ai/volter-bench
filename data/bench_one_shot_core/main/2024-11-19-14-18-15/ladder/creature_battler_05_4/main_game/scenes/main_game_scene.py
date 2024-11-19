from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            else:
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if available_creatures:
                    creatures = [SelectThing(c) for c in available_creatures]
                    back_button = Button("Back")
                    creature_choice = self._wait_for_choice(player, creatures + [back_button])
                    
                    if creature_choice != back_button:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks based on speed
        attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(
                key=lambda x: x[0].active_creature.speed, 
                reverse=True
            )
            
        for attacker, action in attack_actions:
            if attacker.active_creature.hp > 0:  # Only attack if still alive
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, action[1])
                
        # Force swaps for fainted creatures
        for p in [self.player, self.bot]:
            if p.active_creature.hp <= 0:
                self.force_swap(p)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        raw_damage = self.calculate_raw_damage(attacker.active_creature, defender.active_creature, skill)
        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

    def calculate_raw_damage(self, attacker, defender, skill):
        if skill.is_physical:
            return attacker.attack + skill.base_damage - defender.defense
        else:
            return (attacker.sp_attack / defender.sp_defense) * skill.base_damage

    def get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.active_creature.display_name} fainted! Choose next creature:")
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        for p in [self.player, self.bot]:
            if all(c.hp <= 0 for c in p.creatures):
                winner = self.bot if p == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False
