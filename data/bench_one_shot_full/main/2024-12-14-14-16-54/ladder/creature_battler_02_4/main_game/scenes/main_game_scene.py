from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_player_skill = None
        self.queued_opponent_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.queued_player_skill = self._wait_for_choice(self.player, choices).thing

            # Opponent Choice Phase
            choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.queued_opponent_skill = self._wait_for_choice(self.opponent, choices).thing

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                if self.check_battle_end():
                    break
            else:
                break

        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.queued_player_skill), (self.opponent, self.queued_opponent_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.queued_opponent_skill), (self.player, self.queued_player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.queued_player_skill), (self.opponent, self.queued_opponent_skill)
            return (self.opponent, self.queued_opponent_skill), (self.player, self.queued_player_skill)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False
