from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Player's turn:
{self._get_skill_choices_str(self.player_creature)}

Opponent's turn:
{self._get_skill_choices_str(self.opponent_creature)}
"""

    def _get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            if self._check_battle_end():
                self.battle_ended = True
                self._show_battle_result()
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self._apply_damage(self.opponent_creature, player_skill)
        self._apply_damage(self.player_creature, foe_skill)

    def _apply_damage(self, target: Creature, skill: Skill):
        target.hp = max(0, target.hp - skill.damage)

    def _check_battle_end(self) -> bool:
        return self.player_creature.hp == 0 or self.opponent_creature.hp == 0

    def _show_battle_result(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
