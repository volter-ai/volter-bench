from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "Battle start!")
        while True:
            if self._is_battle_over():
                break
            player_choice = self._player_choice_phase()
            opponent_choice = self._foe_choice_phase()
            self._resolution_phase(player_choice, opponent_choice)

        self._show_battle_result()
        self._transition_to_scene("MainMenuScene")

    def _is_battle_over(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices)

    def _foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, choices)

    def _resolution_phase(self, player_choice, opponent_choice):
        first, second = self._determine_order(player_choice, opponent_choice)
        self._execute_skill(*first)
        if not self._is_battle_over():
            self._execute_skill(*second)

    def _determine_order(self, player_choice, opponent_choice):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, player_choice), (self.opponent, self.opponent_creature, opponent_choice)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, opponent_choice), (self.player, self.player_creature, player_choice)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, player_choice), (self.opponent, self.opponent_creature, opponent_choice)
            else:
                return (self.opponent, self.opponent_creature, opponent_choice), (self.player, self.player_creature, player_choice)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill_choice: SelectThing):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
        skill: Skill = skill_choice.thing

        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

    def _get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and creature_type == "leaf":
            return 2
        elif skill_type == "fire" and creature_type == "water":
            return 0.5
        elif skill_type == "water" and creature_type == "fire":
            return 2
        elif skill_type == "water" and creature_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and creature_type == "water":
            return 2
        elif skill_type == "leaf" and creature_type == "fire":
            return 0.5
        else:
            return 1

    def _show_battle_result(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
        else:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
