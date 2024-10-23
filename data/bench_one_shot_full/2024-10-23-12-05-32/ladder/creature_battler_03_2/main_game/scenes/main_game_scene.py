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
            
            first, second = self.determine_turn_order(
                (self.player_creature, player_skill),
                (self.opponent_creature, opponent_skill)
            )
            
            for attacker, defender, skill in [first, second]:
                if self.execute_turn(attacker, defender, skill):
                    if self.check_battle_end():
                        return

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def determine_turn_order(self, player_action, opponent_action):
        player_creature, player_skill = player_action
        opponent_creature, opponent_skill = opponent_action
        
        if player_creature.speed > opponent_creature.speed:
            return (player_creature, self.opponent_creature, player_skill), (opponent_creature, self.player_creature, opponent_skill)
        elif opponent_creature.speed > player_creature.speed:
            return (opponent_creature, self.player_creature, opponent_skill), (player_creature, self.opponent_creature, player_skill)
        else:
            if random.choice([True, False]):
                return (player_creature, self.opponent_creature, player_skill), (opponent_creature, self.player_creature, opponent_skill)
            else:
                return (opponent_creature, self.player_creature, opponent_skill), (player_creature, self.opponent_creature, player_skill)

    def execute_turn(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = round(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return defender.hp == 0

    def get_type_factor(self, skill_type: str, defender_type: str):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire" and defender_type == "leaf":
            return 2.0
        elif skill_type == "water" and defender_type == "fire":
            return 2.0
        elif skill_type == "leaf" and defender_type == "water":
            return 2.0
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1.0

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self.end_battle()
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            self.end_battle()
            return True
        return False

    def end_battle(self):
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
