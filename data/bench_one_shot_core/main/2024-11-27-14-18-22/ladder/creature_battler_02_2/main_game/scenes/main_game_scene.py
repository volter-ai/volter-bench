from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Your turn!")
            self.player_choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Opponent Choice Phase
            self._show_text(self.opponent, "Your turn!")
            self.opponent_choice = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution Phase
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player, self.opponent
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent, self.player
            else:
                first, second = random.choice([(self.player, self.opponent), (self.opponent, self.player)])

            # Execute attacks
            self.execute_attack(self.player_creature, self.opponent_creature)
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return

            self.execute_attack(self.opponent_creature, self.player_creature)
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return

    def execute_attack(self, attacker, defender):
        skill = attacker.skills[0]  # For now just use tackle
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= max(0, damage)
