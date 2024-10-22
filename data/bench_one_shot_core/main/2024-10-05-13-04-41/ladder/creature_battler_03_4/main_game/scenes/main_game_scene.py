from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_turn = 0
        self.player_skill = None
        self.opponent_skill = None

    def __str__(self):
        return f"""===Battle===
Turn: {self.current_turn}

{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Choose Skill
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            self.current_turn += 1
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
        first, second = self.determine_turn_order()
        self.execute_skill(first[0], first[1], second[1])
        if second[1].hp > 0:
            self.execute_skill(second[0], second[1], first[1])

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.player_skill), (self.opponent, self.opponent_creature, self.opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.opponent_skill), (self.player, self.player_creature, self.player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_skill), (self.opponent, self.opponent_creature, self.opponent_skill)
            else:
                return (self.opponent, self.opponent_creature, self.opponent_skill), (self.player, self.player_creature, self.player_skill)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature):
        skill = self.player_skill if attacker == self.player else self.opponent_skill
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        type_factor = self.calculate_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def calculate_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self.end_battle(f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self.end_battle(f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def end_battle(self, message: str):
        self._show_text(self.player, message)
        self._transition_to_scene("MainMenuScene")
