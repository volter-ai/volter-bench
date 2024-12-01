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
                first_choice, second_choice = self.player_choice, self.opponent_choice
            elif self.opponent_creature.speed > self.player_creature.speed:
                first, second = self.opponent, self.player
                first_choice, second_choice = self.opponent_choice, self.player_choice
            else:
                if random.random() < 0.5:
                    first, second = self.player, self.opponent
                    first_choice, second_choice = self.player_choice, self.opponent_choice
                else:
                    first, second = self.opponent, self.player
                    first_choice, second_choice = self.opponent_choice, self.player_choice

            # Execute first attack
            self.execute_attack(first, first_choice)
            if self.check_battle_end():
                return

            # Execute second attack
            self.execute_attack(second, second_choice)
            if self.check_battle_end():
                return

    def execute_attack(self, attacker, skill_choice):
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature

        skill = next(s for s in attacking_creature.skills if s.display_name == skill_choice.display_name)
        damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        defending_creature.hp -= max(1, damage)  # Minimum 1 damage

        self._show_text(self.player, f"{attacking_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacking_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.opponent, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
