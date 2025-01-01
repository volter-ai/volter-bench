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
        return f"""===Main Game===
Player: {self.player.display_name} | Creature: {self.player_creature.display_name} | HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent: {self.opponent.display_name} | Creature: {self.opponent_creature.display_name} | HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
"""

    def run(self):
        while self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self.player_choice_phase()
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You win!")
                self._end_game()
                return
            self.foe_choice_phase()
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lose!")
                self._end_game()
                return
            self.resolution_phase()

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        self.opponent_skill = random.choice(self.opponent_creature.skills)

    def resolution_phase(self):
        player_damage = self.calculate_damage(self.player_creature, self.opponent_creature, self.player_skill)
        opponent_damage = self.calculate_damage(self.opponent_creature, self.player_creature, self.opponent_skill)

        self.opponent_creature.hp = max(0, self.opponent_creature.hp - player_damage)
        self.player_creature.hp = max(0, self.player_creature.hp - opponent_damage)

        self._show_text(self.player, f"Player's {self.player_creature.display_name} uses {self.player_skill.display_name} dealing {player_damage} damage!")
        self._show_text(self.opponent, f"Opponent's {self.opponent_creature.display_name} uses {self.opponent_skill.display_name} dealing {opponent_damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = effectiveness * raw_damage

        return max(0, int(final_damage))

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def _end_game(self):
        # Decide whether to transition to another scene or quit the game
        self._transition_to_scene("MainMenuScene")
