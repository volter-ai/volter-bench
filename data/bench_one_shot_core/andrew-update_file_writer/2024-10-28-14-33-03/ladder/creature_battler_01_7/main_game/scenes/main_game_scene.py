from mini_game_engine.engine.lib import AbstractGameScene, Button


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
        while True:
            # Player turn
            self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
            player_skill = self._player_choose_skill(self.player, self.player_creature)

            # Bot turn
            self._show_text(self.bot, f"It's your turn, {self.bot.display_name}!")
            bot_skill = self._player_choose_skill(self.bot, self.bot_creature)

            # Resolve turns
            self._resolve_turn(self.player, self.player_creature, player_skill, self.bot_creature)
            if self._check_battle_end():
                break

            self._resolve_turn(self.bot, self.bot_creature, bot_skill, self.player_creature)
            if self._check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def _player_choose_skill(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self, attacker, attacker_creature, skill, defender_creature):
        defender_creature.hp = max(0, defender_creature.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, f"The opponent's {self.bot_creature.display_name} fainted! You won the battle!")
            return True
        return False
