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

> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Ask player if they want to play again
                play_again_button = Button("Play Again")
                quit_button = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again_button, quit_button])
                
                if choice == play_again_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            else:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, skill)
            
            # Check if defender needs to swap
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    if defender == self.player:
                        creature_choices = [SelectThing(creature) for creature in available_creatures]
                        choice = self._wait_for_choice(defender, creature_choices)
                        defender.active_creature = choice.thing
                        self._show_text(self.player, f"You switched to {choice.thing.display_name}!")
                    else:
                        new_creature = random.choice(available_creatures)
                        defender.active_creature = new_creature
                        self._show_text(self.player, f"Foe switched to {new_creature.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        attacker_name = "You" if attacker == self.player else "Foe"
        defender_name = "you" if defender == self.player else "foe"
        self._show_text(self.player, f"{attacker_name} used {skill.display_name} and dealt {final_damage} damage to {defender_name}!")

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
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
