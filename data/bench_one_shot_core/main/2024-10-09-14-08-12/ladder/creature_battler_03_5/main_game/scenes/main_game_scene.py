from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Choose a skill
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while not self.check_battle_end():
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        self._show_text(self.player, f"{self.opponent.display_name} is choosing a skill...")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if not self.check_battle_end():
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = round(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        attacker_name = self.player.display_name if attacker == self.player_creature else self.opponent.display_name
        defender_name = self.opponent.display_name if attacker == self.player_creature else self.player.display_name
        
        self._show_text(self.player, f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!")
        
        effectiveness = self.get_effectiveness_message(weakness_factor)
        self._show_text(self.player, f"It's {effectiveness}!")
        
        self._show_text(self.player, f"{defender_name}'s {defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2.0
            elif defender_type == "water":
                return 0.5
            else:
                return 1.0
        elif skill_type == "water":
            if defender_type == "fire":
                return 2.0
            elif defender_type == "leaf":
                return 0.5
            else:
                return 1.0
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2.0
            elif defender_type == "fire":
                return 0.5
            else:
                return 1.0
        else:
            return 1.0

    def get_effectiveness_message(self, factor):
        if factor > 1:
            return "super effective"
        elif factor < 1:
            return "not very effective"
        else:
            return "effective"

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._show_text(self.player, "Returning to the main menu...")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._show_text(self.player, "Returning to the main menu...")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
