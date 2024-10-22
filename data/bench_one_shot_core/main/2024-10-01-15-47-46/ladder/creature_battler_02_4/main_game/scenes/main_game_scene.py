from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.players = [self.player, self.opponent]
        self.creatures = [self.player.creatures[0], self.opponent.creatures[0]]
        self.battle_ended = False

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.creatures[0].display_name} (HP: {self.creatures[0].hp}/{self.creatures[0].max_hp})\n"
            f"Opponent: {self.opponent.display_name}\n"
            f"Creature: {self.creatures[1].display_name} (HP: {self.creatures[1].hp}/{self.creatures[1].max_hp})\n"
            f"Available skills:\n" + "\n".join([f"- {skill.display_name}" for skill in self.creatures[0].skills])
        )

    def run(self):
        self._reset_creatures()
        self.battle_ended = False
        while not self.battle_ended:
            self._show_battle_state()
            skills = self._choice_phase()
            self._resolution_phase(skills)
            if self._check_battle_end():
                break
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        for creature in self.creatures:
            creature.hp = creature.max_hp

    def _show_battle_state(self):
        for player, creature in zip(self.players, self.creatures):
            self._show_text(player, f"Your creature: {creature.display_name} (HP: {creature.hp}/{creature.max_hp})")
            opponent = self.players[1] if player == self.players[0] else self.players[0]
            opponent_creature = self.creatures[1] if creature == self.creatures[0] else self.creatures[0]
            self._show_text(player, f"Opponent's creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})")

    def _choice_phase(self) -> list[Skill]:
        skills = []
        for player, creature in zip(self.players, self.creatures):
            choices = [Button(skill.display_name) for skill in creature.skills]
            choice = self._wait_for_choice(player, choices)
            skill = next(skill for skill in creature.skills if skill.display_name == choice.display_name)
            skills.append(skill)
        return skills

    def _resolution_phase(self, skills: list[Skill]):
        order = list(range(2))
        if self.creatures[0].speed < self.creatures[1].speed:
            order.reverse()
        elif self.creatures[0].speed == self.creatures[1].speed:
            random.shuffle(order)

        for i in order:
            if not self.battle_ended:
                attacker, defender = self.players[i], self.players[1-i]
                attacker_creature, defender_creature = self.creatures[i], self.creatures[1-i]
                self._execute_skill(attacker, attacker_creature, skills[i], defender, defender_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        message = f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}!"
        self._show_text(attacker, message)
        self._show_text(defender, message)

    def _check_battle_end(self) -> bool:
        for i, creature in enumerate(self.creatures):
            if creature.hp == 0:
                winner, loser = self.players[1-i], self.players[i]
                self._show_text(winner, "You won the battle!")
                self._show_text(loser, "You lost the battle!")
                self.battle_ended = True
                return True
        return False
