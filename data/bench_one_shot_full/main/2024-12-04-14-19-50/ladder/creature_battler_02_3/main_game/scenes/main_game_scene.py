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
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            self.player_choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            self.opponent_choice = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed:
                self.execute_turn(self.player_creature, self.opponent_creature)
                if self.check_battle_end(): break
                self.execute_turn(self.opponent_creature, self.player_creature)
            elif self.player_creature.speed < self.opponent_creature.speed:
                self.execute_turn(self.opponent_creature, self.player_creature)
                if self.check_battle_end(): break
                self.execute_turn(self.player_creature, self.opponent_creature)
            else:
                if random.random() < 0.5:
                    self.execute_turn(self.player_creature, self.opponent_creature)
                    if self.check_battle_end(): break
                    self.execute_turn(self.opponent_creature, self.player_creature)
                else:
                    self.execute_turn(self.opponent_creature, self.player_creature)
                    if self.check_battle_end(): break
                    self.execute_turn(self.player_creature, self.opponent_creature)
            
            if self.check_battle_end():
                break

    def execute_turn(self, attacker, defender):
        skill = attacker.skills[0]  # Only tackle for now
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

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
