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
        return f"""=== Battle Scene ===
Player: {self.player.display_name} - {player_creature.display_name} (HP: {player_creature.hp})
Opponent: {self.opponent.display_name} - {opponent_creature.display_name} (HP: {opponent_creature.hp})
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in opponent_creature.skills]
        self.opponent_choice = self._wait_for_choice(self.opponent, choices)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.opponent_choice.thing)
        elif opponent_creature.speed > player_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.opponent_choice.thing)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
        else:
            # Randomly decide order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, self.opponent_choice.thing)
            else:
                self.execute_skill(opponent_creature, player_creature, self.opponent_choice.thing)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)

        # Check for battle end condition
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._quit_whole_game()

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")
