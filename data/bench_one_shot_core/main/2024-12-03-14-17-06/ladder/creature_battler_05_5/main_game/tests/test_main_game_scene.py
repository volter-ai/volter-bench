import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.scenes.main_game_scene import MainGameScene
from main_game.main import App
from unittest.mock import patch

def test_main_game_scene_random_run():
    app = App()
    
    for i in range(10):
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 30  # More moves needed for complex battle scene
        
        player = app.create_player(f"test_player_{i}")
        scene = MainGameScene(app, player)
        
        with patch.object(MainGameScene, '_transition_to_scene') as mock_transition, \
             patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
            
            try:
                scene.run()
            except RandomModeGracefulExit:
                print(f"Random mode completed run {i}")
            finally:
                assert mock_transition.called or mock_quit.called
