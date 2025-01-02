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
Player: {self.player.display_name} | HP: {player_creature.hp}/{player_creature.max_hp}
Opponent: {self.opponent.display_name} | HP: {opponent_creature.hp}/{opponent_creature.max_hp}

Your Creature: {player_creature.display_name}
Opponent Creature: {opponent_creature.display_name}
"""

    def run(self):
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self.end_battle(player_creature, opponent_creature)
                break

            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            self.resolve_turn(player_creature, opponent_creature, player_choice.thing, opponent_choice.thing)

    def resolve_turn(self, player_creature: Creature, opponent_creature: Creature, player_skill: Skill, opponent_skill: Skill):
        creatures = [(player_creature, player_skill), (opponent_creature, opponent_skill)]
        creatures.sort(key=lambda x: x[0].speed, reverse=True)

        for creature, skill in creatures:
            if creature.hp > 0:
                target = opponent_creature if creature == player_creature else player_creature
                self.execute_skill(creature, target, skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_resistance_factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_resistance_factor * raw_damage)
        defender.hp = max(defender.hp - final_damage, 0)

    def get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def end_battle(self, player_creature: Creature, opponent_creature: Creature):
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")

        # Reset creatures' states
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

        self._transition_to_scene("MainMenuScene")
