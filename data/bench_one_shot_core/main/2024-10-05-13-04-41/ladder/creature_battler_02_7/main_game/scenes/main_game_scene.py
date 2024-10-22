from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.check_battle_end():
                break

    def player_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # If speeds are equal, randomly choose who goes first
            first_attacker, first_creature, first_skill, first_defender = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent_creature),
                (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            ])
            second_attacker, second_creature, second_skill, second_defender = (
                (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                if first_attacker == self.player else
                (self.player, self.player_creature, player_skill, self.opponent_creature)
            )

            self.execute_skill(first_attacker, first_creature, first_skill, first_defender)
            if second_defender.hp > 0:
                self.execute_skill(second_attacker, second_creature, second_skill, second_defender)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.end_battle()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.end_battle()
            return True
        return False

    def end_battle(self):
        choices = [Button("Return to Main Menu"), Button("Quit Game")]
        choice = self._wait_for_choice(self.player, choices)
        if choice.display_name == "Return to Main Menu":
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
