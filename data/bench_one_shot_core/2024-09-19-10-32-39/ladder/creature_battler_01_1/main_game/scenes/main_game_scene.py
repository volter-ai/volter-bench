from typing import List, Tuple

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue: List[Tuple[Skill, Creature, Creature]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.damage} damage" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player turn
            if not self.player_choice_phase():
                return

            # Bot turn
            self.bot_choice_phase()

            # Resolution phase
            self.resolution_phase()

            if self.check_battle_end():
                return

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()
            return False

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        self.skill_queue.append((skill_choice.thing, self.player_creature, self.bot_creature))
        return True

    def bot_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        skill_choice = self._wait_for_choice(self.bot, skill_choices)
        self.skill_queue.append((skill_choice.thing, self.bot_creature, self.player_creature))

    def resolution_phase(self):
        while self.skill_queue:
            skill, user, target = self.skill_queue.pop(0)
            self.execute_skill(skill, user, target)

    def execute_skill(self, skill: Skill, user: Creature, target: Creature):
        self._show_text(self.player, f"{user.display_name} used {skill.display_name}!")
        target.hp -= skill.damage
        self._show_text(self.player, f"{target.display_name} took {skill.damage} damage!")

    def check_battle_end(self):
        if self.bot_creature.hp <= 0:
            self._show_text(self.player, f"The enemy {self.bot_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
