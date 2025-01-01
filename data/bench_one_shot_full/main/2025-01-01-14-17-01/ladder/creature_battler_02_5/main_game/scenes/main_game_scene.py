from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Player's Creatures:
{self._creature_status(self.player.creatures)}

Opponent's Creatures:
{self._creature_status(self.opponent.creatures)}
"""

    def _creature_status(self, creatures):
        return "\n".join([f"{c.display_name} - HP: {c.hp}/{c.max_hp}" for c in creatures])

    def run(self):
        while True:
            self._player_choice_phase()
            self._foe_choice_phase()
            self._resolution_phase()
            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_choice = choice.thing

    def _foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        self.opponent_choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in opponent_creature.skills]).thing

    def _resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed or randomly if speeds are equal
        if player_creature.speed > opponent_creature.speed:
            self._execute_skill(player_creature, opponent_creature, self.player_choice)
            if opponent_creature.hp > 0:
                self._execute_skill(opponent_creature, player_creature, self.opponent_choice)
        elif player_creature.speed < opponent_creature.speed:
            self._execute_skill(opponent_creature, player_creature, self.opponent_choice)
            if player_creature.hp > 0:
                self._execute_skill(player_creature, opponent_creature, self.player_choice)
        else:
            # Randomly choose which creature goes first
            first, second = random.choice([(player_creature, opponent_creature), (opponent_creature, player_creature)])
            first_choice = self.player_choice if first == player_creature else self.opponent_choice
            second_choice = self.opponent_choice if first == player_creature else self.player_choice

            self._execute_skill(first, second, first_choice)
            if second.hp > 0:
                self._execute_skill(second, first, second_choice)

    def _execute_skill(self, attacker, defender, skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")

    def _check_battle_end(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        if player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
