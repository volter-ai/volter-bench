from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        while not self.battle_ended:
            if self.player_turn():
                if self.check_battle_end():
                    break
            if self.opponent_turn():
                if self.check_battle_end():
                    break
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return self.execute_skill(self.player_creature, self.opponent_creature, choice.thing)

    def opponent_turn(self):
        self._show_text(self.player, f"{self.opponent.display_name}'s turn!")
        skill = random.choice(self.opponent_creature.skills)
        return self.execute_skill(self.opponent_creature, self.player_creature, skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = max(1, int(weakness_factor * raw_damage))  # Ensure at least 1 damage is dealt
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return defender.hp == 0

    def calculate_weakness_factor(self, skill_type: str, defender_type: str):
        if skill_type == defender_type:
            return 1
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self.battle_ended = True
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self.battle_ended = True
            return True
        return False
