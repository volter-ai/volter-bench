from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def get_available_creatures(self, player) -> list:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_knocked_out(self, player) -> bool:
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
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(self.player, skill_choices + [back_button])
                if skill_choice != back_button:
                    player_action = ("attack", skill_choice.thing)
            else:
                creature_choices = [SelectThing(creature) for creature in self.get_available_creatures(self.player)]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(self.player, creature_choices + [back_button])
                if creature_choice != back_button:
                    player_action = ("swap", creature_choice.thing)

            if not player_action:
                continue

            # Bot turn
            if random.random() < 0.2 and self.get_available_creatures(self.opponent):
                bot_action = ("swap", random.choice(self.get_available_creatures(self.opponent)))
            else:
                bot_action = ("attack", random.choice(self.opponent.active_creature.skills))

            # Resolution phase
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
            if bot_action[0] == "swap":
                self.opponent.active_creature = bot_action[1]

            # Handle attacks
            if player_action[0] == "attack" and bot_action[0] == "attack":
                # Determine order
                first = self.player if self.player.active_creature.speed > self.opponent.active_creature.speed else self.opponent
                second = self.opponent if first == self.player else self.player
                first_action = player_action if first == self.player else bot_action
                second_action = bot_action if first == self.player else player_action

                # Execute attacks
                damage = self.calculate_damage(first.active_creature, second.active_creature, first_action[1])
                second.active_creature.hp -= damage
                self._show_text(self.player, f"{first.active_creature.display_name} used {first_action[1].display_name} for {damage} damage!")

                if second.active_creature.hp > 0:
                    damage = self.calculate_damage(second.active_creature, first.active_creature, second_action[1])
                    first.active_creature.hp -= damage
                    self._show_text(self.player, f"{second.active_creature.display_name} used {second_action[1].display_name} for {damage} damage!")

            # Check for knocked out creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_knocked_out(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.opponent.active_creature.hp <= 0:
                if not self.handle_knocked_out(self.opponent):
                    self._show_text(self.player, "You won!")
                    break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
