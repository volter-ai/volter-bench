import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Battle Scene ===
Player's Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent's Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        self.opponent_skill = random.choice(opponent_creature.skills)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        opponent_creature.hp -= self.player_skill.damage
        player_creature.hp -= self.opponent_skill.damage

        if opponent_creature.hp <= 0:
            self._show_text(self.player, "You win!")
            self.reset_creature_states()
            self._quit_whole_game()
        elif player_creature.hp <= 0:
            self._show_text(self.player, "You lose!")
            self.reset_creature_states()
            self._quit_whole_game()

    def reset_creature_states(self):
        """Reset the player's creatures to their initial state."""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
