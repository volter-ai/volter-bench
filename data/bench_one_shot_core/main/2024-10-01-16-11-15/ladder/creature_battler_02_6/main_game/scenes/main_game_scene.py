from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_counter = 0
        self.max_turns = 20  # Limit the number of turns to prevent infinite loops

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.turn_counter += 1
            if self.turn_counter > self.max_turns:
                self._show_text(self.player, "The battle has gone on for too long. It's a draw!")
                self._transition_to_scene("MainMenuScene")
                return

            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self._check_battle_end():
                return

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # If speeds are equal, randomly choose who goes first
            if random.choice([True, False]):
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
