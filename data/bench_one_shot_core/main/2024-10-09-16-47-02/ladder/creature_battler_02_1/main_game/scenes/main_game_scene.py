from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill = None
        self.opponent_skill = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> {', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            self.player_choice_phase()
            self.opponent_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def opponent_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing

    def resolution_phase(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
            if not self.check_battle_end():
                self.execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
            if not self.check_battle_end():
                self.execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
        else:
            # Random determination when speeds are equal
            if random.choice([True, False]):
                self.execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
                if not self.check_battle_end():
                    self.execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
            else:
                self.execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
                if not self.check_battle_end():
                    self.execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Ensure HP is not negative
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
