from typing import List

from main_game.models import Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.foe.display_name}: {self.foe_creature.display_name} (HP: {self.foe_creature.hp}/{self.foe_creature.max_hp})

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, f"Your creature's available skills:\n{self.get_skill_choices_str()}")
            player_skill = self.player_choice_phase()
            self.skill_queue.append(player_skill)

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            self.skill_queue.append(foe_skill)

            # Resolution Phase
            self.resolution_phase()

            # Check for battle end
            if self.check_battle_end():
                break

        # Fallback transition in case the battle somehow ends without triggering the normal end conditions
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                self.foe_creature.hp -= skill.damage
                self._show_text(self.player, f"{self.player_creature.display_name} used {skill.display_name}!")
                self._show_text(self.foe, f"{self.player_creature.display_name} used {skill.display_name}!")
            else:
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"{self.foe_creature.display_name} used {skill.display_name}!")
                self._show_text(self.foe, f"{self.foe_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
