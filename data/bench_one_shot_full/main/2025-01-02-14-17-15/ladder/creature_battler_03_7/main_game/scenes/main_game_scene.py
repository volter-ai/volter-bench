from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Main Game Scene ===
Player: {self.player.display_name} - {player_creature.display_name} (HP: {player_creature.hp})
Opponent: {self.opponent.display_name} - {opponent_creature.display_name} (HP: {opponent_creature.hp})
"""

    def run(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            self.resolve_turn(player_creature, opponent_creature, player_choice.thing, opponent_choice.thing)

            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self.end_battle(player_creature, opponent_creature)
                break

    def resolve_turn(self, player_creature, opponent_creature, player_skill, opponent_skill):
        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_skill)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
        elif opponent_creature.speed > player_creature.speed:
            self.execute_skill(opponent_creature, player_creature, opponent_skill)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_skill)
        else:
            # Randomly decide order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, player_skill)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, opponent_skill)
            else:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, player_skill)

    def execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_resistance_factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = max(0, int(raw_damage * weakness_resistance_factor))
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {final_damage} damage to {defender.display_name}!")

    def get_weakness_resistance_factor(self, skill_type, creature_type):
        # Define type effectiveness
        effectiveness = {
            "normal": {},
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def end_battle(self, player_creature, opponent_creature):
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
        self._quit_whole_game()
