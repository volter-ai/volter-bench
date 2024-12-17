from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Your turn!")
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Opponent choice phase
            self._show_text(self.opponent, "Opponent's turn!")
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution phase
            first, second = self.determine_turn_order()
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                self.check_battle_end()

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def execute_turn(self, acting_player):
        attacker = self.player_creature if acting_player == self.player else self.opponent_creature
        defender = self.opponent_creature if acting_player == self.player else self.player_creature
        skill = attacker.skills[0]  # Using first skill since we don't track which was chosen
        
        damage = skill.base_damage + attacker.attack - defender.defense
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
