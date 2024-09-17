from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Main Game===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.bot.display_name}'s {self.bot.active_creature.display_name}
HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while not self.battle_ended:
            self.turn_counter += 1
            player_action = self.player_turn(self.player)
            bot_action = self.player_turn(self.bot)
            self.resolve_turn(player_action, bot_action)

            if self.check_battle_end():
                self.battle_ended = True

        self._show_text(self.player, "Returning to Main Menu...")
        self._transition_to_scene("MainMenuScene")

    def player_turn(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                action = self.choose_attack(player)
            elif choice == swap_button:
                action = self.choose_swap(player)

            if action is not None:
                return action

    def choose_attack(self, player: Player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def choose_swap(self, player: Player):
        available_creatures = [creature for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        if not available_creatures:
            self._show_text(player, f"No creatures available to swap.")
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [player_action, bot_action]
        actions.sort(key=lambda x: x[0] == "swap", reverse=True)  # Swap actions go first

        for action in actions:
            if action[0] == "swap":
                self.perform_swap(self.player if action == player_action else self.bot, action[1])
            elif action[0] == "attack":
                self.perform_attack(self.player if action == player_action else self.bot, action[1])

        self.check_forced_swap(self.player)
        self.check_forced_swap(self.bot)

    def perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker: Player, skill: Skill):
        defender = self.bot if attacker == self.player else self.player
        attacker_speed = attacker.active_creature.speed
        defender_speed = defender.active_creature.speed

        if attacker_speed > defender_speed or (attacker_speed == defender_speed and random.choice([True, False])):
            self.execute_attack(attacker, defender, skill)
        else:
            self.execute_attack(defender, attacker, defender.active_creature.skills[0])  # Defender attacks first with their first skill
            if attacker.active_creature.hp > 0:  # Only attack if attacker's creature is still alive
                self.execute_attack(attacker, defender, skill)

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_forced_swap(self, player: Player):
        if player.active_creature.hp == 0:
            available_creatures = [creature for creature in player.creatures if creature.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} has been knocked out!")
                new_creature = self.force_swap(player, available_creatures)
                self.perform_swap(player, new_creature)
            else:
                self._show_text(player, f"{player.display_name} has no more creatures available!")

    def force_swap(self, player: Player, available_creatures: List[Creature]) -> Creature:
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, "Choose a creature to swap in:")
        choice = self._wait_for_choice(player, creature_choices)
        return choice.thing

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
