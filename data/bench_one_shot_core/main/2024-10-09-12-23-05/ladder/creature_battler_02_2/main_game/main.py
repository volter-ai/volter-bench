import uuid
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player
from mini_game_engine.engine.lib import OnGameStart


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)
        self._current_scene = None

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

    def transition_to_scene(self, scene_id: str, **kwargs):
        scene_factory = self.scene_registry[scene_id]
        self._current_scene = scene_factory(app=self, **kwargs)
        self.__run_scene(self._current_scene)

    def __run_scene(self, scene):
        if len(self._scene_stack) == 1:
            AbstractApp.broadcast_event(OnGameStart())

        self._show_changes()

        scene.run()

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
