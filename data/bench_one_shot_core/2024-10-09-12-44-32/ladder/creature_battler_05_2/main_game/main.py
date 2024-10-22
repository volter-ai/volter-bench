import uuid

from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import AbstractApp, BotListener, HumanListener


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)
        self.human_player = None
        self.bot_player = None

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str):
        bot = Player.from_prototype_id(prototype_id=prototype_id)
        bot.uid = str(uuid.uuid4())
        bot.set_listener(BotListener())
        return bot

    def run(self, player: Player):
        self.human_player = player
        self.bot_player = self.create_bot("basic_opponent")
        super().run(player)

    def transition_to_scene(self, scene_id: str, **kwargs):
        if scene_id == "MainGameScene":
            kwargs["player"] = self.human_player
            kwargs["bot"] = self.bot_player
        super().transition_to_scene(scene_id, **kwargs)

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
