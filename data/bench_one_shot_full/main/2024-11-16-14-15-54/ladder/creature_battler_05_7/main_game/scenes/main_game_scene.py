from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Player
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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Keep getting actions until both players have valid actions
            while True:
                # Player turn
                player_action = self.get_player_action(self.player)
                if not player_action:
                    continue
                    
                # Bot turn
                bot_action = self.get_player_action(self.bot)
                if not bot_action:
                    continue
                    
                # If we got here, both actions are valid
                break
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Determine attack order
        if player_action[0] == "attack" and bot_action[0] == "attack":
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = player_action, bot_action
                first_player, second_player = self.player, self.bot
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = bot_action, player_action
                first_player, second_player = self.bot, self.player
            else:
                if random.random() < 0.5:
                    first, second = player_action, bot_action
                    first_player, second_player = self.player, self.bot
                else:
                    first, second = bot_action, player_action
                    first_player, second_player = self.bot, self.player
                    
            # Execute attacks
            if first[0] == "attack":
                self.execute_attack(first_player, first[1])
            if second[0] == "attack" and second_player.active_creature.hp > 0:
                self.execute_attack(second_player, second[1])

    def execute_attack(self, attacker: Player, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show attack result
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if multiplier > 1:
            self._show_text(attacker, "It's super effective!")
        elif multiplier < 1:
            self._show_text(attacker, "It's not very effective...")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        # Check if all player creatures are fainted
        if all(c.hp <= 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
            
        # Check if all bot creatures are fainted
        if all(c.hp <= 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is fainted
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(self.player, choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp <= 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self.bot.active_creature = random.choice(available)
                
        return False
