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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
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
            self._show_text(self.opponent, "Opponent's turn!")
            self.opponent_choice = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution Phase
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player, self.opponent
                first_creature, second_creature = self.player_creature, self.opponent_creature
                first_choice, second_choice = self.player_choice, self.opponent_choice
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent, self.player
                first_creature, second_creature = self.opponent_creature, self.player_creature
                first_choice, second_choice = self.opponent_choice, self.player_choice
            else:
                if random.random() < 0.5:
                    first, second = self.player, self.opponent
                    first_creature, second_creature = self.player_creature, self.opponent_creature
                    first_choice, second_choice = self.player_choice, self.opponent_choice
                else:
                    first, second = self.opponent, self.player
                    first_creature, second_creature = self.opponent_creature, self.player_creature
                    first_choice, second_choice = self.opponent_choice, self.player_choice

            # Execute first attack
            damage = first_creature.attack + first_creature.skills[0].base_damage - second_creature.defense
            second_creature.hp -= max(1, damage)
            self._show_text(self.player, f"{first_creature.display_name} used {first_choice.display_name}!")
            
            if second_creature.hp <= 0:
                if second == self.player:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return

            # Execute second attack
            damage = second_creature.attack + second_creature.skills[0].base_damage - first_creature.defense
            first_creature.hp -= max(1, damage)
            self._show_text(self.player, f"{second_creature.display_name} used {second_choice.display_name}!")

            if first_creature.hp <= 0:
                if first == self.player:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
