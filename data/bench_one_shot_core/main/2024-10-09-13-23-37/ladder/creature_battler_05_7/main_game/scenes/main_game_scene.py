from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_turn()
            if self._check_battle_end():
                break
            self._bot_turn()
            if self._check_battle_end():
                break
            self._resolve_turn()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        action = self._get_player_action(self.player)
        self.turn_queue.append((self.player, action))

    def _bot_turn(self):
        self._show_text(self.player, f"{self.bot.display_name} is choosing an action...")
        action = self._get_player_action(self.bot)
        self.turn_queue.append((self.bot, action))

    def _get_player_action(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                return self._choose_skill(current_player)
            elif swap_button == choice:
                return self._choose_swap(current_player)

    def _choose_skill(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self._get_player_action(current_player)
        return choice.thing

    def _choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c != current_player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self._get_player_action(current_player)
        return choice.thing

    def _resolve_turn(self):
        # Sort the turn queue by speed, with random tiebreaker for equal speeds
        self.turn_queue.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for player, action in self.turn_queue:
            if isinstance(action, Creature):
                self._swap_creature(player, action)
            elif isinstance(action, Skill):
                self._use_skill(player, action)
                self._check_and_swap_fainted_creature(self.player)
                self._check_and_swap_fainted_creature(self.bot)

        self.turn_queue.clear()

    def _swap_creature(self, player, new_creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")

    def _use_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        weakness_factor = self._get_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * weakness_factor)  # Explicit conversion to integer

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} on {defender.display_name}'s {defender_creature.display_name} for {final_damage} damage!")

    def _get_weakness_factor(self, skill_type, defender_type):
        weakness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return weakness_chart.get(skill_type, {}).get(defender_type, 1)

    def _check_and_swap_fainted_creature(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = available_creatures[0]
                self._swap_creature(player, new_creature)
            else:
                self._show_text(self.player, f"{player.display_name} has no more creatures available!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have been defeated. {self.bot.display_name} wins!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, f"All of {self.bot.display_name}'s creatures have been defeated. You win!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
