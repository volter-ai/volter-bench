from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import AbstractApp, HumanListener


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def transition_to_scene(self, scene_id: str, **kwargs):
        # Reset creature states before transitioning
        if "player" in kwargs:
            player = kwargs["player"]
            for creature in player.creatures:
                creature.hp = creature.max_hp

        scene_factory = self.scene_registry[scene_id]
        scene = scene_factory(app=self, **kwargs)
        self.__run_scene(scene)

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
