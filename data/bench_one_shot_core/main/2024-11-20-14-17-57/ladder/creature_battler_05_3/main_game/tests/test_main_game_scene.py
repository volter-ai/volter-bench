import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from unittest.mock import patch

def test_main_game_scene_random_run():
    app = App()
    
    for i in range(10):
        print(f"Starting random run iteration {i}")
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 30  # More moves needed for battle scene
        
        player = app.create_player(f"player_{i}")
        scene = MainGameScene(app, player)
        
        # Mock the transition method to prevent actual scene transitions during unit test
        with patch.object(MainGameScene, '_transition_to_scene') as mock_transition:
            try:
                scene.run()
            except RandomModeGracefulExit:
                print(f"Random mode completed successfully for run {i}")
            
            # Verify that the scene attempted to transition when it ended
            assert mock_transition.called
            assert mock_transition.call_args[0][0] == "MainMenuScene"
