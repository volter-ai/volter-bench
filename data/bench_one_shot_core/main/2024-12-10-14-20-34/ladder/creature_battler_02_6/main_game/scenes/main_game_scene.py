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
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills])

            # Opponent choice phase
            self.opponent_choice = self._wait_for_choice(self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills])

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player, self.opponent
            elif self.opponent_creature.speed > self.player_creature.speed:
                first, second = self.opponent, self.player
            else:
                first, second = random.choice([(self.player, self.opponent), (self.opponent, self.player)])

            # Execute moves
            self.execute_turn(first, second)

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def execute_turn(self, first, second):
        # Get creatures and skills
        first_creature = self.player_creature if first == self.player else self.opponent_creature
        second_creature = self.player_creature if second == self.player else self.opponent_creature
        
        first_skill = first_creature.skills[0]  # Using tackle for now since it's the only skill
        second_skill = second_creature.skills[0]

        # Calculate and apply damage
        first_damage = max(0, first_creature.attack + first_skill.base_damage - second_creature.defense)
        second_creature.hp -= first_damage
        self._show_text(first, f"{first_creature.display_name} used {first_skill.display_name} for {first_damage} damage!")

        if second_creature.hp > 0:
            second_damage = max(0, second_creature.attack + second_skill.base_damage - first_creature.defense)
            first_creature.hp -= second_damage
            self._show_text(second, f"{second_creature.display_name} used {second_skill.display_name} for {second_damage} damage!")
