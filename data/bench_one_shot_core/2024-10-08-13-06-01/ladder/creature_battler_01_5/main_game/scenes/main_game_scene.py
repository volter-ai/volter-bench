from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self._check_battle_end():
                self._end_battle()
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.foe, f"Opponent's {self.player_creature.display_name} used {player_skill.display_name}!")

        self.player_creature.hp -= foe_skill.damage
        self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")
        self._show_text(self.foe, f"Your {self.foe_creature.display_name} used {foe_skill.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False

    def _end_battle(self):
        self._reset_creatures()
        self._show_text(self.player, "Returning to main menu...")
        self._show_text(self.foe, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
