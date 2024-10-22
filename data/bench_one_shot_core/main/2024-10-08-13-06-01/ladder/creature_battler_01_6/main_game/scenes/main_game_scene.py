from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


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

Opponent's skills:
{self._format_skills(self.bot_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild bot appeared!")
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()

            # Bot Choice Phase
            bot_skill = self._bot_choice_phase()

            # Resolution Phase
            self._resolution_phase(player_skill, bot_skill)

            if self._check_battle_end():
                self._end_battle()
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _bot_choice_phase(self):
        self._show_text(self.bot, "Bot is choosing a skill...")
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, bot_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.bot, f"Bot used {bot_skill.display_name}!")

        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"You dealt {player_skill.damage} damage!")
        self._show_text(self.bot, f"Bot dealt {bot_skill.damage} damage!")

    def _check_battle_end(self):
        return self.player_creature.hp <= 0 or self.bot_creature.hp <= 0

    def _end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
