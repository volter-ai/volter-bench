from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

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
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            foe_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, foe_skill)

            if self.check_battle_end():
                break

        self.reset_creatures()

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} used {foe_skill.display_name}!")
        self.player_creature.hp -= foe_skill.damage

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
