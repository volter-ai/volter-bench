from mini_game_engine.engine.lib import AbstractGameScene, Button
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

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while not self.battle_ended:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()
            self.resolve_turn(player_skill, opponent_skill)
            if self.check_battle_end():
                break
        self.end_battle()

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        self._show_text(self.player, f"{self.opponent.display_name}'s available skills:")
        for skill in self.opponent_creature.skills:
            self._show_text(self.player, f"- {skill.display_name}")
        chosen_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent.display_name} chose {chosen_skill.display_name}!")
        return chosen_skill

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if second.hp > 0:
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1: Creature, creature2: Creature):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}!")

    def get_type_factor(self, skill_type: str, defender_type: str):
        if skill_type == "normal":
            return 1
        elif skill_type == defender_type:
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
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self.battle_ended = True
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            self.battle_ended = True
            return True
        return False

    def end_battle(self):
        self._show_text(self.player, "The battle has ended!")
        choices = [Button("Return to Main Menu"), Button("Quit Game")]
        choice = self._wait_for_choice(self.player, choices)
        if choice.display_name == "Return to Main Menu":
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
