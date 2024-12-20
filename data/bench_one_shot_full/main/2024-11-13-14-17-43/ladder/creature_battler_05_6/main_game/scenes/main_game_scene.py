from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
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
            player_action = self.get_player_action(self.player)
            if not player_action:  # Player chose Back at top level
                continue
                
            bot_action = self.get_player_action(self.bot)
            self.resolve_turn(player_action, bot_action)
            
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        while True:
            valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            
            # Top level choices
            choices = [Button("Attack")]
            if valid_creatures:
                choices.append(Button("Swap"))
            if player != self.bot:  # Only show Back to human player
                choices.append(Button("Back"))
                
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Back":
                return None
            elif choice.display_name == "Attack":
                action = self.get_attack_choice(player)
                if action:  # None means Back was chosen
                    return action
            else:  # Swap
                action = self.get_swap_choice(player, valid_creatures)
                if action:  # None means Back was chosen
                    return action

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        if player != self.bot:
            choices.append(Button("Back"))
            
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return {"type": "attack", "skill": choice.thing}

    def get_swap_choice(self, player, valid_creatures):
        choices = [SelectThing(creature) for creature in valid_creatures]
        if player != self.bot:
            choices.append(Button("Back"))
            
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed > bot_speed:
                first, second = self.player, self.bot
                first_action, second_action = player_action, bot_action
            elif bot_speed > player_speed:
                first, second = self.bot, self.player
                first_action, second_action = bot_action, player_action
            else:
                # Random resolution for speed ties
                if random.choice([True, False]):
                    first, second = self.player, self.bot
                    first_action, second_action = player_action, bot_action
                else:
                    first, second = self.bot, self.player
                    first_action, second_action = bot_action, player_action
            
            # Execute attacks in determined order
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action["skill"])

    def execute_attack(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing

    def check_battle_end(self):
        player_has_valid = any(c.hp > 0 for c in self.player.creatures)
        bot_has_valid = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_valid:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_valid:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
