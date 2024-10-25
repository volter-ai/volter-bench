import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing, find_button
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener


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

    def test_player_wins_two_rounds(self, app, player):
        main_game_scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Round 1: Player chooses Rock, Bot chooses Scissors
        choices = runner.dequeue_wait_for_choice(player)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        assert main_game_scene.player_score == 1
        assert main_game_scene.bot_score == 0

        # Round 2: Player chooses Paper, Bot chooses Rock
        choices = runner.dequeue_wait_for_choice(player)
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        assert main_game_scene.player_score == 2
        assert main_game_scene.bot_score == 0

        # Player chooses to play again
        choices = runner.dequeue_wait_for_choice(player)
        play_again = find_button(choices, "Play Again")
        runner.make_choice(play_again)

        assert runner.dequeue_transition_to_scene() == "MainGameScene"

    def test_bot_wins_two_rounds(self, app, player):
        main_game_scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Round 1: Player chooses Scissors, Bot chooses Rock
        choices = runner.dequeue_wait_for_choice(player)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        assert main_game_scene.player_score == 0
        assert main_game_scene.bot_score == 1

        # Round 2: Player chooses Paper, Bot chooses Scissors
        choices = runner.dequeue_wait_for_choice(player)
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        assert main_game_scene.player_score == 0
        assert main_game_scene.bot_score == 2

        # Player chooses to quit
        choices = runner.dequeue_wait_for_choice(player)
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_three_rounds_with_tie(self, app, player):
        main_game_scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Round 1: Player chooses Rock, Bot chooses Rock (Tie)
        choices = runner.dequeue_wait_for_choice(player)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        assert main_game_scene.player_score == 0
        assert main_game_scene.bot_score == 0

        # Round 2: Player chooses Paper, Bot chooses Rock
        choices = runner.dequeue_wait_for_choice(player)
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        assert main_game_scene.player_score == 1
        assert main_game_scene.bot_score == 0

        # Round 3: Player chooses Scissors, Bot chooses Paper
        choices = runner.dequeue_wait_for_choice(player)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        assert main_game_scene.player_score == 2
        assert main_game_scene.bot_score == 0

        # Player chooses to quit
        choices = runner.dequeue_wait_for_choice(player)
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
