from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
            # Player choice phase
            self._show_text(self.player, "Your turn!")
            self.player_choice = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])

            # Opponent choice phase
            self._show_text(self.opponent, "Your turn!")
            self.opponent_choice = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle ends
                return

            self.execute_turn(second)
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle ends
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_choice), (self.opponent, self.opponent_choice)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.opponent_choice), (self.player, self.player_choice)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_choice), (self.opponent, self.opponent_choice)
            return (self.opponent, self.opponent_choice), (self.player, self.player_choice)

    def execute_turn(self, turn):
        attacker, skill_choice = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill_choice.thing.base_damage - defender_creature.defense
        defender_creature.hp -= max(1, damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill_choice.thing.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False
