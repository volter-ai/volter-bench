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

Player's turn:
{self._get_skill_choices_str(self.player_creature)}
"""

    def _get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.foe, self.foe_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

        self._end_battle()

    def _player_choice_phase(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.foe, f"{self.player_creature.display_name} used {player_skill.display_name}!")

        if self.foe_creature.hp > 0:
            self.player_creature.hp -= foe_skill.damage
            self._show_text(self.player, f"{self.foe_creature.display_name} used {foe_skill.display_name}!")
            self._show_text(self.foe, f"{self.foe_creature.display_name} used {foe_skill.display_name}!")

    def _check_battle_end(self):
        return self.player_creature.hp <= 0 or self.foe_creature.hp <= 0

    def _end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
