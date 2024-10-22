import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from unittest.mock import patch


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # Increased to 30 for more complex scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition:
                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainGameScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called, "scene was not exited in an expected manner"
                    print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    def test_player_wins_battle(self, app):
        player = app.create_player("test_player")
        foe = app.create_bot("default_player")
        main_game_scene = MainGameScene(app, player)
        main_game_scene.foe = foe

        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # First turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 7
        assert main_game_scene.foe_creature.hp == 7

        # Second turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 4
        assert main_game_scene.foe_creature.hp == 4

        # Third turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 1
        assert main_game_scene.foe_creature.hp == 1

        # Fourth turn (player wins)
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 1
        assert main_game_scene.foe_creature.hp == 0
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_player_loses_battle(self, app):
        player = app.create_player("test_player")
        foe = app.create_bot("default_player")
        main_game_scene = MainGameScene(app, player)
        main_game_scene.foe = foe

        # Modify the player's creature to have less HP
        main_game_scene.player_creature.hp = 9
        main_game_scene.player_creature.max_hp = 9

        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # First turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 6
        assert main_game_scene.foe_creature.hp == 7

        # Second turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 3
        assert main_game_scene.foe_creature.hp == 4

        # Third turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert main_game_scene.player_creature.hp == 0
        assert main_game_scene.foe_creature.hp == 1
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
