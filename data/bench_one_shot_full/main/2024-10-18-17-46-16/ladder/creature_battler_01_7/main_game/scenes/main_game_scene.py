from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill_queue: List[Skill] = []
        self.opponent_skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appeared!")
        self.battle_loop()
        self.display_battle_result()
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        self._show_text(self.opponent, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill_queue.append(choice.thing)

    def resolution_phase(self):
        while self.player_skill_queue or self.opponent_skill_queue:
            if self.player_skill_queue:
                player_skill = self.player_skill_queue.pop(0)
                self._show_text(self.player, f"You used {player_skill.display_name}!")
                self.opponent_creature.hp -= player_skill.damage

            if self.opponent_skill_queue:
                opponent_skill = self.opponent_skill_queue.pop(0)
                self._show_text(self.opponent, f"Opponent used {opponent_skill.display_name}!")
                self.player_creature.hp -= opponent_skill.damage

            if self.check_battle_end():
                break

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def display_battle_result(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self.player_skill_queue.clear()
        self.opponent_skill_queue.clear()
