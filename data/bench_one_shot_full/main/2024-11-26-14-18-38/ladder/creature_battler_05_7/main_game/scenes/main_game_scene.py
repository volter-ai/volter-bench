from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature, Skill
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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

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
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                available_creatures = [
                    creature for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creatures = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {self.player.active_creature.display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {self.bot.active_creature.display_name}!")

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
            
        defender = self.bot if attacker == self.player else self.player
        skill = action["skill"]
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")
            
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
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
        
        if not available_creatures:
            winner = "You win!" if player == self.bot else "You lose!"
            self._show_text(self.player, winner)
            self._transition_to_scene("MainMenuScene")
            return
            
        if player == self.player:
            creatures = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creatures)
            player.active_creature = choice.thing
            self._show_text(self.player, f"Go {player.active_creature.display_name}!")
        else:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"Foe sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = "You win!" if bot_has_creatures else "You lose!"
            self._show_text(self.player, winner)
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
