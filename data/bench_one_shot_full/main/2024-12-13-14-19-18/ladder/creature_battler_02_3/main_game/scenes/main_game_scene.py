from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.opponent.display_name}'s {self.opponent_creature.display_name}:
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(
                self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves
            for attacker, creature, skill in [first, second]:
                if self.execute_skill(attacker, creature, skill):
                    return

    def determine_order(self, move1, move2):
        p1_creature = move1[1]
        p2_creature = move2[1]
        
        if p1_creature.speed > p2_creature.speed:
            return move1, move2
        elif p2_creature.speed > p1_creature.speed:
            return move2, move1
        else:
            return (move1, move2) if random.random() < 0.5 else (move2, move1)

    def execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(1, damage)

        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player,
            f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

        if defender_creature.hp <= 0:
            winner = attacker.display_name
            self._show_text(self.player, f"{winner} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
