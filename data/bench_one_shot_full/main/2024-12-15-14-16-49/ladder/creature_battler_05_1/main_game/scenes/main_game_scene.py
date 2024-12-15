from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack - Use a skill
> Swap - Switch active creature
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

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            else:
                # Show available creatures
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.bot, f"Go {bot_action[1].display_name}!")
            
        # Then handle attacks
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if (bot_action[0] == "attack" and player_action[0] == "attack" and
            self.bot.active_creature.speed > self.player.active_creature.speed):
            first = self.bot
            second = self.player
            first_action = bot_action
            second_action = player_action
            
        if first_action[0] == "attack":
            self.execute_attack(first, second, first_action[1])
            
        if second.active_creature.hp > 0 and second_action[0] == "attack":
            self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, 
                                                  defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * effectiveness)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if effectiveness == 2:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness == 0.5:
            self._show_text(attacker, "It's not very effective...")
            
        # Handle fainting
        if defender.active_creature.hp == 0:
            self._show_text(defender, 
                          f"{defender.active_creature.display_name} fainted!")
            self.handle_faint(defender)

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature:")
        creature_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go {choice.thing.display_name}!")

    def reset_creatures(self, player: Player):
        """Reset all creatures' HP to their max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures(self.player)
            self.reset_creatures(self.bot)
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures(self.player)
            self.reset_creatures(self.bot)
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
