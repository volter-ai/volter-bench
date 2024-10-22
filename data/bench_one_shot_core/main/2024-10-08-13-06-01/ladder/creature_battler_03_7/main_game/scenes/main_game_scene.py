from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature, Skill
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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Current Turn: {self.current_turn}
Player Skill: {self.player_skill.display_name if self.player_skill else 'Not chosen'}
Opponent Skill: {self.opponent_skill.display_name if self.opponent_skill else 'Not chosen'}

> Choose Skill
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")
        while True:
            self.current_turn += 1
            self.player_choice_phase()
            self.opponent_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self):
        first, second = self.determine_order()
        self.execute_skill(first[2], first[1], second[2])
        if self.check_battle_end():
            return
        self.execute_skill(second[2], second[1], first[2])

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_skill, self.player_creature), (self.opponent, self.opponent_skill, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_skill, self.opponent_creature), (self.player, self.player_skill, self.player_creature)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_skill, self.player_creature), (self.opponent, self.opponent_skill, self.opponent_creature)
            else:
                return (self.opponent, self.opponent_skill, self.opponent_creature), (self.player, self.player_skill, self.player_creature)

    def execute_skill(self, attacker: Creature, skill: Skill, defender: Creature):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self.calculate_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {final_damage} damage!")

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
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
