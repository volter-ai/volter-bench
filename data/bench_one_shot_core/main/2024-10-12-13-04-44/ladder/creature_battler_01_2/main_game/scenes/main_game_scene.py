from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            bot_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, bot_skill)

            # Check for battle end
            self.check_battle_end()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {player_skill.display_name}!")
        self.bot_creature.hp = max(0, self.bot_creature.hp - player_skill.damage)
        self._show_text(self.bot, f"{self.bot.display_name}'s {self.bot_creature.display_name} uses {bot_skill.display_name}!")
        self.player_creature.hp = max(0, self.player_creature.hp - bot_skill.damage)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.battle_ended = True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.battle_ended = True

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
