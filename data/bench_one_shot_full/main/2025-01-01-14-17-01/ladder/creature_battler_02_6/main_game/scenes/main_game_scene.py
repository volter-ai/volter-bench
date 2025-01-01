import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""===Main Game Scene===
Player: {self.player.display_name} | Creature: {player_creature.display_name} | HP: {player_creature.hp}/{player_creature.max_hp}
Opponent: {self.opponent.display_name} | Creature: {opponent_creature.display_name} | HP: {opponent_creature.hp}/{opponent_creature.max_hp}
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

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
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_choice)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_choice)
        else:
            # Randomly decide order if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, self.player_choice)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
            else:
                self.execute_skill(opponent_creature, player_creature, self.opponent_choice)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, self.player_choice)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage to {defender.display_name}!")

    def end_battle(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()
        else:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
