from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from typing import List
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset all creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team: {', '.join(c.display_name for c in self.player.creatures if c.hp > 0)}
Foe's Team: {', '.join(c.display_name for c in self.bot.creatures if c.hp > 0)}
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After battle ends, give option to return to menu or quit
                menu_button = Button("Return to Menu")
                quit_button = Button("Quit Game")
                choice = self._wait_for_choice(self.player, [menu_button, quit_button])
                
                if choice == menu_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.get_player_action(player)
            return {"type": "attack", "skill": skill_choice.thing}
            
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self.get_player_action(player)
            return {"type": "swap", "creature": creature_choice.thing}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        self.execute_action(first_action[0], first_action[1])
        
        if second_action[1]["type"] == "attack" and second_action[0].active_creature.hp > 0:
            self.execute_action(second_action[0], second_action[1])

    def get_action_order(self, player_action, bot_action):
        if player_action["type"] == "swap" or bot_action["type"] == "swap":
            return (self.player, player_action), (self.bot, bot_action)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed or (player_speed == bot_speed and random.random() < 0.5):
            return (self.player, player_action), (self.bot, bot_action)
        return (self.bot, bot_action), (self.player, player_action)

    def execute_action(self, attacker, action):
        if action["type"] != "attack":
            return
            
        skill = action["skill"]
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness} Dealt {final_damage} damage!")
        
        # Handle fainting
        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender_creature.display_name} was knocked out!")
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, 
                f"{'You' if player == self.player else 'Foe'} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
