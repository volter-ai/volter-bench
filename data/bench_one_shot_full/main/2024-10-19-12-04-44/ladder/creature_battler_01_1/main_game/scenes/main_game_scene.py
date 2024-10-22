from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
from typing import List, Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False
        self.skill_queue: List[Tuple[Player, Creature, Skill, Player, Creature]] = []

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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        self._show_text(self.opponent, f"A wild {self.player_creature.display_name} appears!")

        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self._player_turn(self.player, self.player_creature)
            self.skill_queue.append((self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature))

            # Foe Choice Phase
            opponent_skill = self._player_turn(self.opponent, self.opponent_creature)
            self.skill_queue.append((self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature))

            # Resolution Phase
            self._resolve_queued_skills()

            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_turn(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolve_queued_skills(self):
        while self.skill_queue:
            attacker, attacker_creature, skill, defender, defender_creature = self.skill_queue.pop(0)
            self._resolve_skill(attacker, attacker_creature, skill, defender, defender_creature)
            if self._check_battle_end():
                break

    def _resolve_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        defender_creature.hp = max(0, defender_creature.hp - skill.damage)
        self._show_text(attacker, f"Your {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"The opponent's {attacker_creature.display_name} used {skill.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self.battle_ended = True
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self.battle_ended = True
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
