import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App
from main_game.scenes.main_menu_scene import MainMenuScene

def test_main_menu_scene_random():
    for i in range(10):
        app = App()
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 10
        
        player = app.create_player(f"test_player_{i}")
        scene = MainMenuScene(app, player)
        
        try:
            scene.run()
        except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
            print(f"Random run {i} completed successfully")
