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
Player Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in opponent_creature.skills]
        self.foe_choice = self._wait_for_choice(self.opponent, choices)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine execution order
        if player_creature.speed > opponent_creature.speed:
            first, second = (self.player_choice, player_creature, opponent_creature), (self.foe_choice, opponent_creature, player_creature)
        elif player_creature.speed < opponent_creature.speed:
            first, second = (self.foe_choice, opponent_creature, player_creature), (self.player_choice, player_creature, opponent_creature)
        else:
            first, second = random.sample([(self.player_choice, player_creature, opponent_creature), (self.foe_choice, opponent_creature, player_creature)], 2)

        # Execute skills
        for choice, attacker, defender in [first, second]:
            if defender.hp <= 0:
                break
            self.execute_skill(choice.thing, attacker, defender)

    def execute_skill(self, skill: Skill, attacker: Creature, defender: Creature):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense

        # Determine weakness-resistance factor
        factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)

        # Calculate final damage
        final_damage = int(raw_damage * factor)

        # Apply damage
        defender.hp = max(defender.hp - final_damage, 0)

        # Show result
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {final_damage} damage.")

    def get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "normal": {},
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
        self._quit_whole_game()
