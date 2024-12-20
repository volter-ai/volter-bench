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
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_turn(self, first_player: Player, second_player: Player, first_action, second_action):
        # Handle swaps first
        if isinstance(first_action, Creature):
            first_player.active_creature = first_action
        if isinstance(second_action, Creature):
            second_player.active_creature = second_action

        # Handle attacks
        if not isinstance(first_action, Creature):
            damage = self.calculate_damage(first_player.active_creature, second_player.active_creature, first_action)
            second_player.active_creature.hp -= damage
            self._show_text(first_player, f"{first_player.active_creature.display_name} used {first_action.display_name}!")
            self._show_text(first_player, f"Dealt {damage} damage!")

        if not isinstance(second_action, Creature) and second_player.active_creature.hp > 0:
            damage = self.calculate_damage(second_player.active_creature, first_player.active_creature, second_action)
            first_player.active_creature.hp -= damage
            self._show_text(second_player, f"{second_player.active_creature.display_name} used {second_action.display_name}!")
            self._show_text(second_player, f"Dealt {damage} damage!")

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def force_swap(self, player: Player):
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Player choice phase
            choices = [Button("Attack")]
            
            # Only add swap option if there are creatures to swap to
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
                
            player_choice = self._wait_for_choice(self.player, choices)

            player_action = None
            if player_choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                player_action = self._wait_for_choice(self.player, skill_choices).thing
            else:
                creature_choices = [SelectThing(c) for c in available_creatures]
                player_action = self._wait_for_choice(self.player, creature_choices).thing

            # Bot choice phase
            bot_action = None
            available_bot_creatures = self.get_available_creatures(self.bot)
            if not available_bot_creatures or random.random() < 0.8:  # 80% chance to attack or if no swaps available
                bot_action = random.choice(self.bot.active_creature.skills)
            else:
                bot_action = random.choice(available_bot_creatures)

            # Resolution phase
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self.handle_turn(self.player, self.bot, player_action, bot_action)
            else:
                self.handle_turn(self.bot, self.player, bot_action, player_action)

            # Check for KOs and force swaps
            if self.player.active_creature.hp <= 0:
                if not self.force_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    break
                    
            if self.bot.active_creature.hp <= 0:
                if not self.force_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self._transition_to_scene("MainMenuScene")
