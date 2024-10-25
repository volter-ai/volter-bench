from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Choose a skill
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.description}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        battle_result = self.battle_loop()
        self.display_battle_result(battle_result)
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            bot_skill = self.bot_choice_phase()
            self.resolution_phase(player_skill, bot_skill)

            if self.player_creature.hp <= 0:
                return "lose"
            elif self.bot_creature.hp <= 0:
                return "win"

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def bot_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.bot, f"Opponent used {bot_skill.display_name}!")

        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"You dealt {player_skill.damage} damage!")
        self._show_text(self.player, f"You received {bot_skill.damage} damage!")

    def display_battle_result(self, result: str):
        if result == "win":
            self._show_text(self.player, "Congratulations! You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle. Better luck next time!")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
