from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.battle_result = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        self.battle_loop()
        self.display_battle_result()
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            bot_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, bot_skill)

            if self.check_battle_end():
                return

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} used {bot_skill.display_name}!")
        self.player_creature.hp -= bot_skill.damage

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self.battle_result = "lose"
            return True
        elif self.bot_creature.hp <= 0:
            self.battle_result = "win"
            return True
        return False

    def display_battle_result(self):
        if self.battle_result == "win":
            self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} fainted! You win!")
        elif self.battle_result == "lose":
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
