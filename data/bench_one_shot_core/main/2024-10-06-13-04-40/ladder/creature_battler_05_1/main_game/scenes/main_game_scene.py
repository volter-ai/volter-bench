from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.player_choice_phase(self.player)
            bot_action = self.player_choice_phase(self.bot)
            self.resolution_phase(player_action, bot_action)

            if self.check_battle_end():
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def player_choice_phase(self, current_player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(current_player, choices)

        if attack_button == choice:
            return self.choose_attack(current_player)
        elif swap_button == choice:
            return self.choose_swap(current_player)

    def choose_attack(self, current_player: Player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player: Player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("swap", choice.thing)

    def resolution_phase(self, player_action, bot_action):
        actions = [player_action, bot_action]
        players = [self.player, self.bot]

        # Handle swaps first
        for i, action in enumerate(actions):
            if action[0] == "swap":
                self.perform_swap(players[i], action[1])

        # Sort actions by speed, using a random value to break ties
        actions_with_speed = [
            (action, player, player.active_creature.speed, random.random())
            for action, player in zip(actions, players)
        ]
        sorted_actions = sorted(actions_with_speed, key=lambda x: (x[2], x[3]), reverse=True)

        for action, player, _, _ in sorted_actions:
            if action[0] == "attack":
                self.perform_attack(player, action[1])

    def perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker: Player, skill: Skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
