from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        while True:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()
            if self.resolve_turn(player_skill, opponent_skill):
                break

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        opponent_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} is preparing to use {opponent_skill.display_name}!")
        return opponent_skill

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        first_attacker, second_attacker = self.determine_turn_order()
        
        first_skill = player_skill if first_attacker == self.player_creature else opponent_skill
        second_skill = opponent_skill if first_attacker == self.player_creature else player_skill
        
        first_defender = self.opponent_creature if first_attacker == self.player_creature else self.player_creature
        second_defender = self.player_creature if first_attacker == self.player_creature else self.opponent_creature

        if self.execute_skill(first_attacker, first_defender, first_skill):
            return True

        if self.execute_skill(second_attacker, second_defender, second_skill):
            return True

        return False

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player_creature, self.opponent_creature
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent_creature, self.player_creature
        else:
            return random.choice([(self.player_creature, self.opponent_creature), (self.opponent_creature, self.player_creature)])

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return self.check_battle_end()

    def get_type_factor(self, skill_type: str, defender_type: str):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and defender_type == "leaf":
            return 2
        elif skill_type == "water" and defender_type == "fire":
            return 2
        elif skill_type == "leaf" and defender_type == "water":
            return 2
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp == 0 or self.opponent_creature.hp == 0:
            self.end_battle()
            return True
        return False

    def end_battle(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
        
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
