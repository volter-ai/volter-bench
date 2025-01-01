from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Battle ===
Your Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent's Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!" if opponent_creature.hp <= 0 else "You lost!")
                self._reset_creatures_state(self.player)
                self._transition_to_scene("MainMenuScene")
                break

            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            player_creature.hp -= opponent_choice.thing.damage
            opponent_creature.hp -= player_choice.thing.damage

    def _reset_creatures_state(self, player: Player):
        for creature in player.creatures:
            creature.hp = creature.max_hp
