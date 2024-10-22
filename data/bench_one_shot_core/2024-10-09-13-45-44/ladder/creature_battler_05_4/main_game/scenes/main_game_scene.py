import random
from typing import List, Tuple, Union

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.action_queue: List[Tuple[Player, Union[Skill, Tuple[str, Creature]]]] = []
        self.initialize_battle()

    def initialize_battle(self):
        self.player.active_creature = self.player.creatures[0] if self.player.creatures else None
        self.bot.active_creature = self.bot.creatures[0] if self.bot.creatures else None

    def __str__(self):
        player_creature = f"{self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})" if self.player.active_creature else "No active creature"
        bot_creature = f"{self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})" if self.bot.active_creature else "No active creature"
        return f"""===Battle===
{self.player.display_name}: {player_creature}
{self.bot.display_name}: {bot_creature}

> Attack
> Swap
"""

    def run(self):
        while True:
            if self.check_battle_end():
                self.end_battle()
                break
            self.player_turn()
            if self.check_battle_end():
                self.end_battle()
                break
            self.bot_turn()
            if self.check_battle_end():
                self.end_battle()
                break
            self.resolution_phase()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self.choose_skill(self.player)
                if skill:
                    self.action_queue.append((self.player, skill))
                    return
            elif choice == swap_button:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.action_queue.append((self.player, ("swap", new_creature)))
                    return

    def bot_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button, back_button]
            choice = random.choice(choices[:2])  # Bot only chooses between Attack and Swap

            if choice == attack_button:
                skill = self.choose_skill(self.bot)
                if skill:
                    self.action_queue.append((self.bot, skill))
                    return
            elif choice == swap_button:
                new_creature = self.choose_creature(self.bot)
                if new_creature:
                    self.action_queue.append((self.bot, ("swap", new_creature)))
                    return

    def choose_skill(self, player):
        if not player.active_creature:
            return None
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def resolution_phase(self):
        # Sort action queue based on creature speed or swap priority
        self.action_queue.sort(key=lambda x: (
            -1 if isinstance(x[1], tuple) else x[0].active_creature.speed,
            random.random()  # For random resolution of equal speed
        ), reverse=True)

        for player, action in self.action_queue:
            if isinstance(action, tuple) and action[0] == "swap":
                self.swap_creature(player, action[1])
            elif isinstance(action, Skill):
                opponent = self.bot if player == self.player else self.player
                self.execute_skill(player, opponent, action)

        self.action_queue.clear()

    def swap_creature(self, player, new_creature):
        player.active_creature = new_creature
        if new_creature:
            self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def execute_skill(self, attacker, defender, skill):
        if not attacker.active_creature or not defender.active_creature:
            return
        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack) + float(skill.base_damage) - float(defender.active_creature.defense)
        else:
            raw_damage = (float(attacker.active_creature.sp_attack) / float(defender.active_creature.sp_defense)) * float(skill.base_damage)

        weakness_factor = float(self.calculate_weakness(skill.skill_type, defender.active_creature.creature_type))
        final_damage = int(weakness_factor * raw_damage)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_weakness(self, skill_type, creature_type):
        weaknesses = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return weaknesses.get(skill_type, {}).get(creature_type, 1.0)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self.choose_creature(player) if player == self.player else random.choice(available_creatures)
            self.swap_creature(player, new_creature)
        else:
            self.swap_creature(player, None)

    def check_battle_end(self):
        if not self.player.active_creature or all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if not self.bot.active_creature or all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def end_battle(self):
        self._show_text(self.player, "The battle has ended!")
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
