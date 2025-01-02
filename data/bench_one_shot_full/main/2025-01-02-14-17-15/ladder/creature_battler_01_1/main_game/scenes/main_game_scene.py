from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __str__(self):
        return f"===Main Game===\nPlayer: {self.player.display_name}\nOpponent: Bot\n"

    def run(self):
        player_creature = self.player.creatures[0]
        bot = self._app.create_bot("default_player")
        bot_creature = bot.creatures[0]

        while player_creature.hp > 0 and bot_creature.hp > 0:
            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            bot_choice = self._wait_for_choice(bot, [SelectThing(skill) for skill in bot_creature.skills])

            # Resolve choices
            bot_creature.hp -= player_choice.thing.damage
            player_creature.hp -= bot_choice.thing.damage

            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
            elif bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")

        # Reset player's creatures' state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp

        self._transition_to_scene("MainMenuScene")
