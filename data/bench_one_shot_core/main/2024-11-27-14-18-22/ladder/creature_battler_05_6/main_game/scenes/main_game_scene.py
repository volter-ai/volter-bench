from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
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

What will you do?
> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_bot_action()
            
            # Resolution phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Transition back to menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = []
        for skill in player.active_creature.skills:
            choice = DictionaryChoice(skill.display_name)
            choice.value = {"type": "attack", "skill": skill}
            choices.append(choice)
            
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return choice.value

    def get_swap_choice(self, player):
        choices = []
        for creature in player.creatures:
            if creature != player.active_creature and creature.hp > 0:
                choice = DictionaryChoice(creature.display_name)
                choice.value = {"type": "swap", "creature": creature}
                choices.append(choice)
                
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return choice.value

    def get_bot_action(self):
        # Simple bot AI - randomly attack or swap if possible
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return {"type": "attack", "skill": skill}
        else:
            available_creatures = [c for c in self.bot.creatures 
                                 if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return {"type": "swap", "creature": random.choice(available_creatures)}
            else:
                skill = random.choice(self.bot.active_creature.skills)
                return {"type": "attack", "skill": skill}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action), (self.bot, bot_action)
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action), (self.player, player_action)
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action), (self.bot, bot_action)
                else:
                    first, second = (self.bot, bot_action), (self.player, player_action)
                    
            self.execute_attack(first[0], first[1]["skill"])
            if self.bot.active_creature.hp > 0:
                self.execute_attack(second[0], second[1]["skill"])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
            attacker_name = "You"
        else:
            defender = self.player
            attacker_name = "Foe"
            
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
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
                       f"{attacker_name} used {skill.display_name}! "
                       f"Dealt {final_damage} damage!")

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
        # Check if either player has any creatures left
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is fainted
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                self._show_text(self.player, f"{self.player.active_creature.display_name} fainted!")
                swap_choice = self.get_swap_choice(self.player)
                if swap_choice:
                    self.player.active_creature = swap_choice["creature"]
                    
        if self.bot.active_creature.hp <= 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self._show_text(self.player, f"Foe's {self.bot.active_creature.display_name} fainted!")
                self.bot.active_creature = random.choice(available)
                self._show_text(self.player, f"Foe sent out {self.bot.active_creature.display_name}!")
                
        return False
