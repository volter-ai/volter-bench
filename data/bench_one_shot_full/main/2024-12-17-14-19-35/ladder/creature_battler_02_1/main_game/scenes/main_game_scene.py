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

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def execute_turn(self, first, second):
        # First attacker
        attacker = first.creatures[0]
        defender = second.creatures[0]
        skill = first.creatures[0].skills[0]  # Using tackle
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= max(1, damage)
        self._show_text(first, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(second, f"{defender.display_name} took {damage} damage!")

        if defender.hp > 0:
            # Second attacker
            attacker = second.creatures[0]
            defender = first.creatures[0]
            skill = second.creatures[0].skills[0]  # Using tackle
            damage = attacker.attack + skill.base_damage - defender.defense
            defender.hp -= max(1, damage)
            self._show_text(second, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(first, f"{defender.display_name} took {damage} damage!")
