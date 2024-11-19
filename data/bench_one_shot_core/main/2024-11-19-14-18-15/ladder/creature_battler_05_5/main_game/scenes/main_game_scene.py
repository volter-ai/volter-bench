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
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if skill_choice.display_name != "Back":
                    return ("attack", skill_choice.display_name)
                
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if available_creatures:
                    available_creatures.append(Button("Back"))
                    swap_choice = self._wait_for_choice(player, available_creatures)
                    
                    if not isinstance(swap_choice, Button):
                        return ("swap", swap_choice.thing)

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
            
        for player, action in attack_actions:
            if player.active_creature.hp > 0:  # Only attack if still alive
                self.execute_attack(player, action[1])

    def execute_attack(self, attacker, skill_name):
        defender = self.bot if attacker == self.player else self.player
        
        skill = next(s for s in attacker.active_creature.skills if s.display_name == skill_name)
        
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
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )
        
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.handle_faint(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            swap_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {choice.thing.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp == 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, 
                    f"{winner.display_name} wins the battle!"
                )
                self._transition_to_scene("MainMenuScene")
                return True
        return False
