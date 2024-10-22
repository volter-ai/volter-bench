import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing, find_button
from mini_game_engine.engine.lib import HumanListener


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        HumanListener.random_mode = True

        for i in range(10):
            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)
            runner = ThreadedSceneRunner()
            runner.start_game(main_game_scene)

            # Run through the game events
            for event in runner.iterate_game_events():
                if event['type'] == 'choice_request':
                    choices = event['choices']
                    runner.make_choice(choices[0])  # Always choose the first option in random mode
                elif event['type'] == 'scene_transition':
                    break  # End of game

            # Assert that the game ended (transitioned to a new scene)
            assert event['type'] == 'scene_transition'
            assert main_game_scene.player_score + main_game_scene.bot_score <= 3
            assert main_game_scene.player_score <= 2 and main_game_scene.bot_score <= 2

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    def test_player_wins_two_rounds_and_plays_again(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 1
        assert scene.player_score == 0
        assert scene.bot_score == 0
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.player_score == 1
        assert scene.bot_score == 0
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        # Game end
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.player_score == 2
        assert scene.bot_score == 0
        play_again = find_button(choices, "Play Again")
        runner.make_choice(play_again)

        assert runner.dequeue_transition_to_scene() == "MainGameScene"

    def test_bot_wins_two_rounds_and_player_quits(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 1
        assert scene.player_score == 0
        assert scene.bot_score == 0
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.player_score == 0
        assert scene.bot_score == 1
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        # Game end
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.player_score == 0
        assert scene.bot_score == 2
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_three_rounds_with_tie_player_wins_and_quits(self, app):
        player = app.create_player("test_player")
        scene = MainGameScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 1
        assert scene.player_score == 0
        assert scene.bot_score == 0
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 2
        assert scene.player_score == 0
        assert scene.bot_score == 0
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        rock = find_select_thing(choices, "rock")
        runner.make_choice(rock)

        # Round 3
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 3
        assert scene.player_score == 1
        assert scene.bot_score == 0
        scissors = find_select_thing(choices, "scissors")
        runner.make_choice(scissors)

        choices = runner.dequeue_wait_for_choice(scene.bot)
        paper = find_select_thing(choices, "paper")
        runner.make_choice(paper)

        # Game end
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.rounds == 3
        assert scene.player_score == 2
        assert scene.bot_score == 0
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
