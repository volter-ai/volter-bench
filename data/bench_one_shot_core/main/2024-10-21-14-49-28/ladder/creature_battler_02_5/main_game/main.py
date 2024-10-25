import uuid
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from main_game.models import Player
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.battle_result_scene import BattleResultScene


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)
        self.register_scene("BattleResultScene", BattleResultScene)
        self.current_scene = None

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
        scene = scene_factory(app=self, previous_scene=self.current_scene, **kwargs)
        self.current_scene = scene
        self.__run_scene(scene)

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
