from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
{self.bot.display_name}'s {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Check if active creatures need to be swapped
            if self.player.active_creature.hp <= 0:
                if not self.force_swap(self.player):
                    if self.handle_battle_end():
                        return
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.force_swap(self.bot):
                    if self.handle_battle_end():
                        return
                    break

            # Get actions
            player_action = self.get_player_action(self.player)
            if not player_action:  # Player chose back at main menu
                continue
                
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end after each turn
            if self.check_battle_end():
                if self.handle_battle_end():
                    return

    def handle_battle_end(self):
        """Handle end of battle and return True if game should end"""
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
        
        self._transition_to_scene("MainMenuScene")
        return True

    def force_swap(self, player):
        """Force player to swap when active creature is knocked out. Returns False if no swaps available."""
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(player, f"Go {player.active_creature.display_name}!")
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go {player.active_creature.display_name}!")
        return True

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            return None
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills with Back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            choices = skill_choices + [back_button]
            
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self.get_player_action(player)
            return choice
            
        else:  # Swap chosen
            # Show available creatures for swap with Back option
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, "No other creatures available to swap!")
                return self.get_player_action(player)
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            choices = creature_choices + [back_button]
            
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self.get_player_action(player)
            return choice

    def resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"Go {player_action.thing.display_name}!")
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.bot, f"Go {bot_action.thing.display_name}!")
            
        # Skip attack phase if either creature was swapped out
        if isinstance(player_action.thing, Creature) or isinstance(bot_action.thing, Creature):
            return
            
        # Determine attack order for skills
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            first, second = (self.player, player_action), (self.bot, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            first, second = (self.bot, bot_action), (self.player, player_action)
        else:
            if random.random() < 0.5:
                first, second = (self.player, player_action), (self.bot, bot_action)
            else:
                first, second = (self.bot, bot_action), (self.player, player_action)
                    
        # Execute attacks
        self.execute_attack(first[0], first[1].thing, second[0])
        if second[0].active_creature.hp > 0:
            self.execute_attack(second[0], second[1].thing, first[0])

    def execute_attack(self, attacker, skill, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = max(1, int(raw_damage * multiplier))
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show attack result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        return not player_has_creatures or not bot_has_creatures
