from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        battle_result = self.battle_loop()
        self.display_battle_result(battle_result)
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            # Check for battle end
            battle_result = self.check_battle_end()
            if battle_result:
                return battle_result

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first_attacker, first_skill, second_attacker, second_skill = (
                self.player, player_skill, self.opponent, foe_skill
            )
        elif self.player_creature.speed < self.opponent_creature.speed:
            first_attacker, first_skill, second_attacker, second_skill = (
                self.opponent, foe_skill, self.player, player_skill
            )
        else:
            # If speeds are equal, randomly choose who goes first
            if random.choice([True, False]):
                first_attacker, first_skill, second_attacker, second_skill = (
                    self.player, player_skill, self.opponent, foe_skill
                )
            else:
                first_attacker, first_skill, second_attacker, second_skill = (
                    self.opponent, foe_skill, self.player, player_skill
                )

        self.execute_skill(first_attacker, first_attacker.creatures[0], first_skill, second_attacker.creatures[0])
        if second_attacker.creatures[0].hp > 0:
            self.execute_skill(second_attacker, second_attacker.creatures[0], second_skill, first_attacker.creatures[0])

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            return "lose"
        elif self.opponent_creature.hp <= 0:
            return "win"
        return None

    def display_battle_result(self, result):
        if result == "win":
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
        elif result == "lose":
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
