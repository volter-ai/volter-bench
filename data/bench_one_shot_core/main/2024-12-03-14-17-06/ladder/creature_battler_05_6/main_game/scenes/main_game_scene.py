from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Active: {self.player.active_creature.display_name} ({self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP)
Foe's Active: {self.bot.active_creature.display_name} ({self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP)

Your Team:
{player_creatures_status}

Foe's Team:
{bot_creatures_status}

> Attack
> Swap"""

    def reset_creatures(self):
        """Reset all creatures to full HP before leaving scene"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                if self.check_battle_end():
                    self.reset_creatures()
                    self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                if self.check_battle_end():
                    self.reset_creatures()
                    self._quit_whole_game()
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()
                self._quit_whole_game()

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            if not self.handle_fainted_creature(player):
                return None
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        skill_choices = [
            SelectThing(skill) 
            for skill in player.active_creature.skills
        ]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
            
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return self.get_player_action(player)
            
        creature_choices = [
            SelectThing(creature)
            for creature in available_creatures
        ]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
            
        return {"type": "swap", "creature": choice.thing}

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return False
            
        creature_choices = [
            SelectThing(creature)
            for creature in available_creatures
        ]
        
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You swapped to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe swapped to {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order
            first = self.player
            second = self.bot
            first_action = player_action
            second_action = bot_action
            
            if (self.bot.active_creature.speed > self.player.active_creature.speed or 
                (self.bot.active_creature.speed == self.player.active_creature.speed and 
                 random.random() < 0.5)):
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action
                
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action["skill"])

    def execute_attack(self, attacker, defender, skill):
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
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
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
