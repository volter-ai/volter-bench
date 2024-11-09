from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
            # Check for battle end before actions
            if self.check_battle_end():
                # Properly end the game when battle is over
                self._quit_whole_game()
                return

            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def get_player_action(self, player):
        # First check if we can do anything
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if not valid_creatures:
                return {"type": "none"}  # No possible actions
            # Must swap if active creature is fainted
            return self.get_swap_choice(player)

        # Get available choices
        choices = []
        if player.active_creature.hp > 0:  # Can only attack if active creature is alive
            choices.append(Button("Attack"))
        
        # Can only swap if there are valid creatures to swap to
        valid_swap_targets = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if valid_swap_targets:
            choices.append(Button("Swap"))

        if not choices:
            return {"type": "none"}  # No possible actions

        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        return {"type": "attack", "skill": self._wait_for_choice(player, choices).thing}

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not valid_creatures:
            # If no valid swap targets, fall back to attack if possible
            if player.active_creature.hp > 0:
                return self.get_attack_choice(player)
            return {"type": "none"}  # No possible actions
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        return {"type": "swap", "creature": self._wait_for_choice(player, choices).thing}

    def resolve_turn(self, player_action, bot_action):
        # Skip if either player has no valid actions
        if player_action["type"] == "none" or bot_action["type"] == "none":
            return

        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Compare speeds to determine order
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed > bot_speed:
                # Player is faster
                self.execute_attack(self.player, self.bot, player_action["skill"])
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_action["skill"])
            elif bot_speed > player_speed:
                # Bot is faster
                self.execute_attack(self.bot, self.player, bot_action["skill"])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_action["skill"])
            else:
                # Equal speed - randomly decide who goes first
                first_attacker, first_action, second_attacker, second_action = random.choice([
                    (self.player, player_action["skill"], self.bot, bot_action["skill"]),
                    (self.bot, bot_action["skill"], self.player, player_action["skill"])
                ])
                
                self.execute_attack(first_attacker, second_attacker, first_action)
                if second_attacker.active_creature.hp > 0:
                    self.execute_attack(second_attacker, first_attacker, second_action)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")

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
        player_has_valid = any(c.hp > 0 for c in self.player.creatures)
        bot_has_valid = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_valid:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_valid:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
