from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        while True:
            player_skill = self.player_turn()
            bot_skill = self.bot_turn()
            
            if self.execute_turn(player_skill, bot_skill):
                break

        self.end_battle()

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def bot_turn(self):
        bot_skill = random.choice(self.bot_creature.skills)
        self._show_text(self.player, f"{self.bot_creature.display_name} is preparing to use {bot_skill.display_name}!")
        return bot_skill

    def execute_turn(self, player_skill, bot_skill):
        first_attacker, first_skill, second_attacker, second_skill = self.determine_order(
            (self.player_creature, player_skill),
            (self.bot_creature, bot_skill)
        )

        battle_ended = self.execute_skill(first_attacker, second_attacker, first_skill)
        if not battle_ended:
            battle_ended = self.execute_skill(second_attacker, first_attacker, second_skill)

        return battle_ended

    def determine_order(self, pair1, pair2):
        creature1, skill1 = pair1
        creature2, skill2 = pair2
        if creature1.speed > creature2.speed or (creature1.speed == creature2.speed and random.choice([True, False])):
            return creature1, skill1, creature2, skill2
        else:
            return creature2, skill2, creature1, skill1

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return self.check_battle_end()

    def calculate_weakness(self, skill_type: str, defender_type: str) -> float:
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

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def end_battle(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
