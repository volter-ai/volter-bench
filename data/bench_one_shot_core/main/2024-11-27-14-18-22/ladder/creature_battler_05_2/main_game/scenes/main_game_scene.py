from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
                continue
                
            # Bot turn - bot must return an action
            bot_action = self.get_player_action(self.bot, is_bot=True)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.initialize_battle()  # Reset state before leaving
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player, is_bot=False):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        # Only show back button to human players
        choices = [attack_button, swap_button]
        if not is_bot:
            back_button = Button("Back")
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            if not is_bot:
                skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if not is_bot and choice == back_button:
                return None
            return {"type": "attack", "skill": choice.thing}
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return {"type": "attack", "skill": player.active_creature.skills[0]}  # Default to first skill
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            if not is_bot:
                creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if not is_bot and choice == back_button:
                return None
            return {"type": "swap", "creature": choice.thing}

    def resolve_actions(self, player_action, bot_action):
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You sent out {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {bot_action['creature'].display_name}!")

        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first[0], first[1])
        
        if second[0].active_creature.hp > 0:  # Only if target still alive
            self.execute_action(second[0], second[1])

    def determine_order(self, player_action, bot_action):
        if player_action["type"] == "swap" or bot_action["type"] == "swap":
            return (self.player, player_action), (self.bot, bot_action)
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (self.player, player_action), (self.bot, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return (self.bot, bot_action), (self.player, player_action)
        else:
            if random.random() < 0.5:
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
        
        # Show message
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.handle_faint(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if player == self.player:
            self._show_text(self.player, "Choose your next creature!")
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"Foe sent out {player.active_creature.display_name}!")

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
