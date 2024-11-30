from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your options:
> Attack
> Swap
"""

    def run(self):
        while True:
            # Check for battle end before each turn
            if not any(c.hp > 0 for c in self.player.creatures):
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
            elif not any(c.hp > 0 for c in self.bot.creatures):
                self._show_text(self.player, "You won the battle!")
                self._transition_to_scene("MainMenuScene")
            
            # Get player action
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

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
            return ("attack", skill_choice.thing)
            
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                # If no creatures available to swap to, force an attack
                return self.get_player_action(player)
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self.get_player_action(player)
            return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")
            
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
                else:
                    first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
                    
            self.execute_attack(first[0], first[1])
            if self.bot.active_creature.hp > 0 and self.player.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            attacking_creature = self.player.active_creature
            defending_creature = self.bot.active_creature
        else:
            attacking_creature = self.bot.active_creature
            defending_creature = self.player.active_creature
            
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        else:
            raw_damage = (attacking_creature.sp_attack / defending_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defending_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defending_creature.hp = max(0, defending_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f"{attacking_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defending_creature.display_name}!")
        
        # Handle fainting
        if defending_creature.hp <= 0:
            self._show_text(self.player, f"{defending_creature.display_name} was knocked out!")
            self.handle_faint(self.player if defending_creature == self.player.active_creature else self.bot)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            self._show_text(self.player, "Choose next creature:")
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {choice.thing.display_name}!")
