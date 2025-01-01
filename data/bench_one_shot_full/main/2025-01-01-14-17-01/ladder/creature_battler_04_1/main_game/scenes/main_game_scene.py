from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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

Choose a skill:
"""

    def run(self):
        self.battle_loop()

    def battle_loop(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        while player_creature.hp > 0 and opponent_creature.hp > 0:
            self._show_text(self.player, str(self))
            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            self.resolve_turn(player_creature, opponent_creature, player_choice.thing, opponent_choice.thing)

        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
        else:
            self._show_text(self.player, "You won!")

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self, player_creature: Creature, opponent_creature: Creature, player_skill: Skill, opponent_skill: Skill):
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
            # Random order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, player_skill)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, opponent_skill)
            else:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, player_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire" and defender.creature_type == "leaf":
            effectiveness = 2.0
        elif skill.skill_type == "water" and defender.creature_type == "fire":
            effectiveness = 2.0
        elif skill.skill_type == "leaf" and defender.creature_type == "water":
            effectiveness = 2.0
        elif skill.skill_type == "fire" and defender.creature_type == "water":
            effectiveness = 0.5
        elif skill.skill_type == "water" and defender.creature_type == "leaf":
            effectiveness = 0.5
        elif skill.skill_type == "leaf" and defender.creature_type == "fire":
            effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
