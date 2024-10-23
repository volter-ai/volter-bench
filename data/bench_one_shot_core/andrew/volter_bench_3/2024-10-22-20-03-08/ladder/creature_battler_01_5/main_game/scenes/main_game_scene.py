from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while not self.battle_ended:
            player_skill = self.player_choice_phase()
            foe_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, foe_skill)

            if self.check_battle_end():
                self.battle_ended = True

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.foe, f"{self.player_creature.display_name} used {player_skill.display_name}!")

        if self.foe_creature.hp > 0:
            self.player_creature.hp -= foe_skill.damage
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")
            self._show_text(self.foe, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")

    def check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
