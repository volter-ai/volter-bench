from typing import Dict, List, Optional, Tuple
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            
            # Bot Choice Phase
            bot_action = self.get_player_action(self.bot)
            
            # Resolution Phase
            self.resolve_actions(player_action.value, bot_action.value)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, current_player: Player) -> DictionaryChoice:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                action = DictionaryChoice("action")
                action.value = {
                    "type": "attack",
                    "skill": skill_choice.thing
                }
                return action
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [
                    c for c in current_player.creatures 
                    if c != current_player.active_creature and c.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                
                action = DictionaryChoice("action")
                action.value = {
                    "type": "swap",
                    "creature": creature_choice.thing
                }
                return action

    def resolve_actions(self, player_action: Dict, bot_action: Dict):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {self.player.active_creature.display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {self.bot.active_creature.display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            first = self.player
            second = self.bot
            first_action = player_action
            second_action = bot_action
            
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and random.random() < 0.5):
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action
            
            # Execute attacks in order
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:  # Only if target still alive
                self.execute_attack(second, first, second_action["skill"])

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")
        
        # Handle knockouts
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player: Player):
        # Check for available creatures
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            creature_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, 
                f"{'You' if player == self.player else 'Foe'} sent out {player.active_creature.display_name}!")

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
