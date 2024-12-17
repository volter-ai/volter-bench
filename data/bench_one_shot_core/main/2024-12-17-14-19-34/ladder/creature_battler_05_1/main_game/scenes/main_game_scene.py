from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def get_damage_multiplier(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self.get_damage_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def execute_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks based on speed
        if isinstance(player_action.thing, Skill) and isinstance(bot_action.thing, Skill):
            first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action

            # Execute first attack
            damage = self.calculate_damage(first.active_creature, second.active_creature, first_action.thing)
            second.active_creature.hp -= damage
            self._show_text(self.player, f"{first.active_creature.display_name} used {first_action.thing.display_name}!")
            self._show_text(self.player, f"Dealt {damage} damage!")

            # Execute second attack if creature still alive
            if second.active_creature.hp > 0:
                damage = self.calculate_damage(second.active_creature, first.active_creature, second_action.thing)
                first.active_creature.hp -= damage
                self._show_text(self.player, f"{second.active_creature.display_name} used {second_action.thing.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted_creature(self, player: Player) -> bool:
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            player_action = None
            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                player_action = self._wait_for_choice(self.player, skill_choices)
            else:
                creature_choices = [SelectThing(c) for c in self.get_available_creatures(self.player)]
                if creature_choices:
                    player_action = self._wait_for_choice(self.player, creature_choices)

            # Bot turn - randomly choose attack or swap
            bot_action = None
            if random.random() < 0.8:  # 80% chance to attack
                bot_action = SelectThing(random.choice(self.bot.active_creature.skills))
            else:
                available = self.get_available_creatures(self.bot)
                if available:
                    bot_action = SelectThing(random.choice(available))

            # Execute turn if both players made valid choices
            if player_action and bot_action:
                self.execute_turn(player_action, bot_action)

            # Check for fainted creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self._transition_to_scene("MainMenuScene")
