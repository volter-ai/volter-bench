from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
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
        return "\n".join([f"{creature.display_name}: {creature.hp}/{creature.max_hp} HP" for creature in creatures])

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                self._quit_whole_game()
                break

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_choice = choice.thing

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        self.opponent_choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in opponent_creature.skills]).thing

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed or randomly if speeds are equal
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_choice)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_choice)
        else:
            # Randomly decide who goes first if speeds are equal
            first, second = random.choice([(player_creature, opponent_creature), (opponent_creature, player_creature)])
            first_choice = self.player_choice if first == player_creature else self.opponent_choice
            second_choice = self.opponent_choice if second == opponent_creature else self.player_choice

            self.execute_skill(first, second, first_choice)
            if second.hp > 0:
                self.execute_skill(second, first, second_choice)

    def execute_skill(self, attacker, defender, skill):
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(defender.hp - damage, 0)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")

    def check_battle_end(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        if player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
