import uuid
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener, create_from_game_database
from main_game.models import Player
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = create_from_game_database("default_player", Player)
        player.uid = player_id
        player.set_listener(HumanListener())
        if player.creatures:
            player.active_creature = player.creatures[0]
        return player

    def create_bot(self, prototype_id: str):
        bot = create_from_game_database(prototype_id, Player)
        bot.uid = str(uuid.uuid4())
        bot.set_listener(BotListener())
        if bot.creatures:
            bot.active_creature = bot.creatures[0]
        return bot

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
