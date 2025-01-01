from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}
Player Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            if self.opponent.creatures[0].hp <= 0:
                break
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

    def player_choice_phase(self):
        creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        creature = self.opponent.creatures[0]
        self.opponent_skill = random.choice(creature.skills)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed, randomize if speeds are equal
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_skill)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_skill)
        else:
            # Randomize order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, self.player_skill)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
            else:
                self.execute_skill(opponent_creature, player_creature, self.opponent_skill)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, self.player_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        factor = self.calculate_weakness_resistance(skill.skill_type, defender.creature_type)
        final_damage = int(factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {final_damage} damage!")

    def calculate_weakness_resistance(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def end_battle(self):
        if self.player.creatures[0].hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._transition_to_scene("MainMenuScene")
