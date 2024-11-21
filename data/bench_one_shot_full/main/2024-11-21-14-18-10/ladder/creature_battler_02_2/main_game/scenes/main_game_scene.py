from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

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

            # Foe Choice Phase
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
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature

                damage = creature.attack + skill.base_damage - defender_creature.defense
                defender_creature.hp -= max(1, damage)

                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = "You" if attacker == self.player else "Opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, move1, move2):
        p1_creature = move1[1]
        p2_creature = move2[1]
        
        if p1_creature.speed > p2_creature.speed:
            return move1, move2
        elif p1_creature.speed < p2_creature.speed:
            return move2, move1
        else:
            return (move1, move2) if random.random() < 0.5 else (move2, move1)
