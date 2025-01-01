from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Your Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp}/{self.player.creatures[0].max_hp})
Opponent Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp}/{self.opponent.creatures[0].max_hp})
"""

    def run(self):
        self.battle_loop()
        self.reset_creatures()

    def battle_loop(self):
        while True:
            player_choice = self._wait_for_choice(self.player, self.get_skill_choices(self.player.creatures[0]))
            opponent_choice = self._wait_for_choice(self.opponent, self.get_skill_choices(self.opponent.creatures[0]))

            self.resolve_turn(player_choice, opponent_choice)

            if self.is_battle_over():
                break

    def get_skill_choices(self, creature: Creature):
        return [SelectThing(skill) for skill in creature.skills]

    def resolve_turn(self, player_choice: SelectThing, opponent_choice: SelectThing):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine execution order
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_choice.thing)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
        elif opponent_creature.speed > player_creature.speed:
            self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_choice.thing)
        else:
            # Randomly decide order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, player_choice.thing)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
            else:
                self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, player_choice.thing)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * effectiveness)

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

    def is_battle_over(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        if player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
