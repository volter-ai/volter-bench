from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Skill
from typing import List, Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Tuple[Player, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Foe's skills:
{self._format_skills(self.foe_creature.skills)}

Skill Queue:
{self._format_skill_queue()}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def _format_skill_queue(self):
        return "\n".join([f"{player.display_name}: {skill.display_name}" for player, skill in self.skill_queue])

    def run(self):
        while True:
            self._player_turn()
            self._foe_turn()
            self._resolve_turn()

            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_turn(self):
        self._show_text(self.player, "Your turn! Choose a skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def _foe_turn(self):
        self._show_text(self.foe, "Foe's turn! Choose a skill:")
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append((self.foe, choice.thing))

    def _resolve_turn(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            if attacker == self.player:
                target = self.foe_creature
            else:
                target = self.player_creature
            self._apply_damage(attacker, target, skill)

    def _apply_damage(self, attacker, target, skill):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage to {target.display_name}!")
        self._show_text(self.foe, f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage to {target.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
        self._show_text(self.foe, "All creatures have been restored to full health.")
