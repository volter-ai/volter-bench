import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_count = 0

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_count}

{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            self.turn_count += 1
            
            # Player turn
            player_skill = self.player_choice_phase()
            
            # Opponent turn
            opponent_skill = self.opponent_choice_phase()
            
            # Resolution phase
            self.resolution_phase(player_skill, opponent_skill)
            
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, skill_choices).thing

    def opponent_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, skill_choices).thing

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = self.player, self.opponent
            first_skill, second_skill = player_skill, opponent_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = self.opponent, self.player
            first_skill, second_skill = opponent_skill, player_skill
        else:
            # Random decision for equal speeds
            if random.choice([True, False]):
                first, second = self.player, self.opponent
                first_skill, second_skill = player_skill, opponent_skill
            else:
                first, second = self.opponent, self.player
                first_skill, second_skill = opponent_skill, player_skill

        first_creature = first.creatures[0]
        second_creature = second.creatures[0]

        self.execute_skill(first, first_creature, first_skill, second_creature)
        if not self.check_battle_end():
            self.execute_skill(second, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)  # Explicitly convert to integer

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
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
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
