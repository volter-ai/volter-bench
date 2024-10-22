from typing import List

from main_game.models import Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill_queue: List[Skill] = []
        self.bot_skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            self.player_choice_phase()
            self.bot_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_state()

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill_queue.append(choice.thing)

    def bot_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.bot_skill_queue.append(choice.thing)

    def resolution_phase(self):
        while self.player_skill_queue or self.bot_skill_queue:
            if self.player_skill_queue:
                player_skill = self.player_skill_queue.pop(0)
                self._show_text(self.player, f"You used {player_skill.display_name}!")
                self.bot_creature.hp -= player_skill.damage

            if self.bot_skill_queue:
                bot_skill = self.bot_skill_queue.pop(0)
                self._show_text(self.player, f"The wild {self.bot_creature.display_name} used {bot_skill.display_name}!")
                self.player_creature.hp -= bot_skill.damage

            if self.check_battle_end():
                break

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"The wild {self.bot_creature.display_name} fainted. You won!")
            return True
        return False

    def reset_state(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self.player_skill_queue.clear()
        self.bot_skill_queue.clear()
        self._transition_to_scene("MainMenuScene")
