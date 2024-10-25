from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, HumanListener


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

Your skills:
{self._format_skills(self.player_creature.skills)}

Foe's skills:
{self._format_skills(self.foe_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.foe, "Battle start!")

        while True:
            player_skill = self._player_choice_phase()
            foe_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, foe_skill)

            if self._check_battle_end():
                break

        self._reset_creatures()

        # Check if we're in a test environment
        if isinstance(self.player._listener, HumanListener) and self.player._listener.random_mode:
            self._quit_whole_game()
        else:
            self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, foe_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.foe, f"Foe used {foe_skill.display_name}!")

        self.foe_creature.hp -= player_skill.damage
        self.player_creature.hp -= foe_skill.damage

        self._show_text(self.player, f"Dealt {player_skill.damage} damage to foe!")
        self._show_text(self.foe, f"Dealt {foe_skill.damage} damage to you!")

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

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
