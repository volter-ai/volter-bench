import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill = None
        self.opponent_skill = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()
        self.handle_battle_end()

    def game_loop(self):
        while True:
            self.player_choice_phase()
            self.opponent_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self):
        first, second = self.determine_turn_order()
        self.execute_skill(first[0], first[1], second[0])
        if second[0].hp > 0:
            self.execute_skill(second[0], second[1], first[0])

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, self.player_skill), (self.opponent_creature, self.opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent_creature, self.opponent_skill), (self.player_creature, self.player_skill)
        else:
            if random.choice([True, False]):
                return (self.player_creature, self.player_skill), (self.opponent_creature, self.opponent_skill)
            else:
                return (self.opponent_creature, self.opponent_skill), (self.player_creature, self.player_skill)

    def execute_skill(self, attacker: Creature, skill: Skill, defender: Creature):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def handle_battle_end(self):
        play_again = Button("Play Again")
        quit_game = Button("Quit Game")
        choices = [play_again, quit_game]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
