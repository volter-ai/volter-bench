from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")

    def __str__(self):
        return f"""===Battle Scene===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Your Creatures:
{self._creature_status(self.player.creatures)}

Opponent's Creatures:
{self._creature_status(self.opponent.creatures)}
"""

    def _creature_status(self, creatures):
        return "\n".join([f"{creature.display_name} - HP: {creature.hp}/{creature.max_hp}" for creature in creatures])

    def run(self):
        while True:
            self._player_choice_phase()
            self._foe_choice_phase()
            self._resolution_phase()
            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        creature = self.player.creatures[0]
        choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in creature.skills])
        self.player_choice = choice.thing

    def _foe_choice_phase(self):
        creature = self.opponent.creatures[0]
        self.opponent_choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in creature.skills]).thing

    def _resolution_phase(self):
        self._apply_skill(self.player_choice, self.opponent.creatures[0])
        self._apply_skill(self.opponent_choice, self.player.creatures[0])

    def _apply_skill(self, skill, target_creature):
        target_creature.hp -= skill.damage
        self._show_text(self.player, f"{skill.display_name} deals {skill.damage} damage to {target_creature.display_name}!")

    def _check_battle_end(self):
        if self.player.creatures[0].hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent.creatures[0].hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
