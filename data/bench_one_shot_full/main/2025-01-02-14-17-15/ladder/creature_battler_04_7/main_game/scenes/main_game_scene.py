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
        return f"""===Battle===
Player's Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent's Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            player_choice = self.player_turn()
            opponent_choice = self.opponent_turn()
            self.resolve_turn(player_choice, opponent_choice)

            if self.opponent.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                break
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                break

        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def opponent_turn(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in opponent_creature.skills]
        return self._wait_for_choice(self.opponent, choices).thing

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_skill)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
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

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(effectiveness * raw_damage)

        # Apply damage
        defender.hp = max(defender.hp - final_damage, 0)

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)
