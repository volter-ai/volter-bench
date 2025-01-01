from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Player's Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent's Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.battle_end_condition()

    def player_choice_phase(self):
        creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed, with random choice for ties
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_skill)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_skill)
        else:
            # Randomly choose which creature goes first in case of a tie
            first, second = random.choice([(player_creature, opponent_creature), (opponent_creature, player_creature)])
            first_skill = self.player_skill if first == player_creature else self.opponent_skill
            second_skill = self.opponent_skill if first == player_creature else self.player_skill

            self.execute_skill(first, second, first_skill)
            if second.hp > 0:
                self.execute_skill(second, first, second_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        final_damage = self.calculate_final_damage(skill, defender, raw_damage)
        defender.hp = max(defender.hp - final_damage, 0)

    def calculate_final_damage(self, skill: Skill, defender: Creature, raw_damage: int) -> int:
        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_effectiveness)

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return effectiveness[skill_type][creature_type]

    def battle_end_condition(self):
        if self.player.creatures[0].hp == 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._quit_whole_game()
