import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from unittest.mock import patch
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing


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

    def test_player_wins(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        scene.foe_creature.hp = 4  # Set bot's creature HP low for quick win

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Bot's turn
        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Bot's turn
        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp > 0
        assert scene.foe_creature.hp <= 0

    def test_player_loses(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        scene.player_creature.hp = 2  # Set player's creature HP low for quick loss

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Bot's turn
        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp <= 0
        assert scene.foe_creature.hp > 0

    def test_multiple_turns(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        scene.player_creature.hp = scene.player_creature.max_hp = 9
        scene.foe_creature.hp = scene.foe_creature.max_hp = 9

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Round 3
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp > 0
        assert scene.foe_creature.hp <= 0
