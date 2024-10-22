from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_result = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()
        self.display_battle_result()
        self._transition_to_scene("MainMenuScene")

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
            self.battle_result = "lose"
            return True
        elif self.foe_creature.hp <= 0:
            self.battle_result = "win"
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp

    def display_battle_result(self):
        if self.battle_result == "win":
            self._show_text(self.player, f"Congratulations! You defeated {self.foe.display_name}'s {self.foe_creature.display_name}!")
        else:
            self._show_text(self.player, f"Oh no! Your {self.player_creature.display_name} was defeated by {self.foe.display_name}'s {self.foe_creature.display_name}.")
        self._show_text(self.player, "Returning to the main menu...")
