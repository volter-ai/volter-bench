from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Player's turn:
> {self.player_creature.skills[0].display_name}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self.check_battle_end():
                break

        # After battle ends, transition back to MainMenuScene
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = (self.player, player_skill), (self.opponent, foe_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = (self.opponent, foe_skill), (self.player, player_skill)
        else:
            # If speeds are equal, randomly decide who goes first
            if random.choice([True, False]):
                first, second = (self.player, player_skill), (self.opponent, foe_skill)
            else:
                first, second = (self.opponent, foe_skill), (self.player, player_skill)

        for attacker, skill in [first, second]:
            if attacker == self.player:
                self.execute_skill(self.player_creature, self.opponent_creature, skill)
            else:
                self.execute_skill(self.opponent_creature, self.player_creature, skill)

            if self.check_battle_end():
                return

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
