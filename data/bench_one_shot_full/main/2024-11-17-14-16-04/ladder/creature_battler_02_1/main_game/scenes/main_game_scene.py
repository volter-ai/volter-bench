from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent Choice Phase
            opponent_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves in order
            for attacker, defender in [first, second]:
                player, creature, skill = attacker
                target_player, target_creature = defender

                damage = creature.attack + skill.base_damage - target_creature.defense
                target_creature.hp -= max(1, damage)  # Minimum 1 damage

                self._show_text(self.player, 
                    f"{player.display_name}'s {creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")

                if target_creature.hp <= 0:
                    winner = player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, move1, move2):
        player1, creature1, _ = move1
        player2, creature2, _ = move2

        if creature1.speed > creature2.speed:
            return (move1, (player2, creature2)), (move2, (player1, creature1))
        elif creature2.speed > creature1.speed:
            return (move2, (player1, creature1)), (move1, (player2, creature2))
        else:
            if random.random() < 0.5:
                return (move1, (player2, creature2)), (move2, (player1, creature1))
            return (move2, (player1, creature1)), (move1, (player2, creature2))
