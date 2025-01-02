from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Main Game Scene ===
Player's Creature: {player_creature.display_name} (HP: {player_creature.hp})
Opponent's Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp})

Choose a skill:
{self._list_skills(player_creature)}
"""

    def _list_skills(self, creature: Creature):
        return "\n".join(f"{i+1}: {skill.display_name}" for i, skill in enumerate(creature.skills))

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self._player_choice_phase()
            self._foe_choice_phase()
            self._resolution_phase()

        self._end_battle()

    def _player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def _foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in opponent_creature.skills]
        self.foe_choice = self._wait_for_choice(self.opponent, choices)

    def _resolution_phase(self):
        # Implement skill resolution logic here
        pass

    def _end_battle(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._quit_whole_game()
