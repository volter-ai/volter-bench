from mini_game_engine.engine.lib import AbstractGameScene, Button, HumanListener


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

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
        self._show_text(self.player, "A wild creature appears!")
        while True:
            if isinstance(self.player._listener, HumanListener) and self.player._listener.random_mode and self.player._listener.random_mode_counter <= 0:
                break

            player_skill = self._player_choice_phase()
            bot_skill = self._bot_choice_phase()
            self._resolution_phase(player_skill, bot_skill)
            
            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _bot_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return next(skill for skill in self.bot_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, bot_skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {player_skill.display_name}!")
        self.bot_creature.hp = max(0, self.bot_creature.hp - player_skill.damage)

        self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} uses {bot_skill.display_name}!")
        self.player_creature.hp = max(0, self.player_creature.hp - bot_skill.damage)

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} fainted! You win!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
