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
        return f"""=== Battle ===
Player: {self.player.display_name} vs Opponent: {self.opponent.display_name}

Your Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            player_choice = self.player_turn()
            opponent_choice = self.opponent_turn()
            self.resolve_turn(player_choice, opponent_choice)
            if self.opponent.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                self._quit_whole_game()
                return
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                self._quit_whole_game()
                return

    def player_turn(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def opponent_turn(self):
        opponent_creature = self.opponent.creatures[0]
        choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in opponent_creature.skills])
        return choice.thing

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

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
            first, second = random.choice([(player_creature, opponent_creature), (opponent_creature, player_creature)])
            first_skill = player_skill if first == player_creature else opponent_skill
            second_skill = opponent_skill if first == player_creature else player_skill

            self.execute_skill(first, second, first_skill)
            if second.hp > 0:
                self.execute_skill(second, first, second_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")
