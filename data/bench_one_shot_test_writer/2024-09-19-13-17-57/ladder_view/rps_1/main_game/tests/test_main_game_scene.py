import pytest
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing, find_button
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener
from unittest.mock import patch
import random


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        HumanListener.random_mode = True

        # Patch the transition_to_scene method
        with patch.object(App, 'transition_to_scene') as mock_transition:
            for i in range(10):
                player = app.create_player(f"player_{i}")
                main_game_scene = MainGameScene(app, player)

                main_game_scene.run()

                # Assert that transition_to_scene was called
                assert mock_transition.called

                # Reset the mock calls for the next iteration
                mock_transition.reset_mock()

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    def test_game_flow(self, app, player):
        scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        for round in range(1, 3):
            # Player's turn
            choices = runner.dequeue_wait_for_choice(player)
            player_choice = find_select_thing(choices, "rock")
            runner.make_choice(player_choice)

            # Bot's turn
            bot_choices = runner.dequeue_wait_for_choice(scene.bot)
            bot_choice = random.choice(bot_choices)
            runner.make_choice(bot_choice)

            # Determine the winner
            if player_choice.thing.display_name == bot_choice.thing.display_name:
                expected_result = "tie"
            elif (
                (player_choice.thing.display_name == "Rock" and bot_choice.thing.display_name == "Scissors") or
                (player_choice.thing.display_name == "Paper" and bot_choice.thing.display_name == "Rock") or
                (player_choice.thing.display_name == "Scissors" and bot_choice.thing.display_name == "Paper")
            ):
                expected_result = "player"
            else:
                expected_result = "bot"

            # Assert the game state
            assert scene.rounds == round
            assert scene.player_score + scene.bot_score <= round
            if expected_result == "player":
                assert scene.player_score > 0
            elif expected_result == "bot":
                assert scene.bot_score > 0

        # Game end
        choices = runner.dequeue_wait_for_choice(player)
        play_again = find_button(choices, "Play Again")
        runner.make_choice(play_again)

        assert runner.dequeue_transition_to_scene() == "MainGameScene"
        assert scene.rounds == 2
        assert scene.player_score + scene.bot_score <= 2
