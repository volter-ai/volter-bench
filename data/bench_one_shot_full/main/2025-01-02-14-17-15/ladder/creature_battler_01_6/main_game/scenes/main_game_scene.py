from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            player_choice = self._wait_for_choice(self.player, self.get_skill_choices(self.player))
            opponent_choice = self._wait_for_choice(self.opponent, self.get_skill_choices(self.opponent))
            self.resolve_turn(player_choice, opponent_choice)

    def get_skill_choices(self, player: Player):
        return [SelectThing(skill) for skill in player.creatures[0].skills]

    def resolve_turn(self, player_choice: SelectThing, opponent_choice: SelectThing):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        opponent_creature.hp -= player_choice.thing.damage
        player_creature.hp -= opponent_choice.thing.damage

        if player_creature.hp <= 0 or opponent_creature.hp <= 0:
            self.end_battle(player_creature.hp > 0)

    def end_battle(self, player_won: bool):
        if player_won:
            self._show_text(self.player, "You won!")
        else:
            self._show_text(self.player, "You lost!")
        
        # Reset creatures' HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

        self._quit_whole_game()
