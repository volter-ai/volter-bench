from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Battle Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Player's Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent's Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.resolve_turn()

        # After the battle ends, display the result and reset creatures
        self.display_battle_result()
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Player chooses a skill
        player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills]).thing

        # Opponent chooses a skill
        opponent_choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in opponent_creature.skills]).thing

        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_choice)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_choice)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, opponent_choice)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_choice)
        else:
            # Randomly decide order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, player_choice)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, opponent_choice)
            else:
                self.execute_skill(opponent_creature, player_creature, opponent_choice)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, player_choice)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate final damage with type effectiveness
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

    def display_battle_result(self):
        if self.player.creatures[0].hp > 0:
            self._show_text(self.player, "Congratulations! You win!")
        else:
            self._show_text(self.player, "You have been defeated. Better luck next time!")

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
