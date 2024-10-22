from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, opponent_skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {player_skill.display_name}!")
        self._show_text(self.opponent, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} uses {opponent_skill.display_name}!")

        self.opponent_creature.hp -= player_skill.damage
        self.player_creature.hp -= opponent_skill.damage

        self.opponent_creature.hp = max(0, self.opponent_creature.hp)
        self.player_creature.hp = max(0, self.player_creature.hp)

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} has been defeated. You lose!")
            self._show_text(self.opponent, f"You defeated {self.player.display_name}'s {self.player_creature.display_name}. You win!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"You defeated {self.opponent.display_name}'s {self.opponent_creature.display_name}. You win!")
            self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} has been defeated. You lose!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
