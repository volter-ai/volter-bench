from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")

    def __str__(self):
        return f"""=== Battle Scene ===
Player: {self.player.display_name}
Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp}/{self.player.creatures[0].max_hp})

Bot: {self.bot.display_name}
Creature: {self.bot.creatures[0].display_name} (HP: {self.bot.creatures[0].hp}/{self.bot.creatures[0].max_hp})
"""

    def run(self):
        while True:
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                self._transition_to_scene("MainMenuScene")
                return
            elif self.bot.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                self._transition_to_scene("MainMenuScene")
                return

            self.player_turn()
            if self.bot.creatures[0].hp <= 0:
                continue

            self.bot_turn()
            if self.player.creatures[0].hp <= 0:
                continue

    def player_turn(self):
        creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.bot.creatures[0].hp -= choice.thing.damage

    def bot_turn(self):
        creature = self.bot.creatures[0]
        choice = self._wait_for_choice(self.bot, [SelectThing(skill) for skill in creature.skills])
        self.player.creatures[0].hp -= choice.thing.damage
