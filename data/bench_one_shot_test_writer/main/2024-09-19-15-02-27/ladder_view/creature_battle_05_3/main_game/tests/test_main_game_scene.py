import pytest
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener
from unittest.mock import patch
from mini_game_engine.engine.lib import RandomModeGracefulExit


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for the complex MainGameScene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainGameScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called or mock_quit.called, "scene was not exited in an expected manner"

                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    @pytest.fixture
    def main_game_scene(self, app, player):
        return MainGameScene(app, player)

    def test_main_game_scene_full_playthrough(self, app, player, main_game_scene):
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Initial state check
        assert player.active_creature.prototype_id == "bubwool"
        assert main_game_scene.bot.active_creature.prototype_id == "scizard"

        while True:
            # Player turn
            choices = runner.dequeue_wait_for_choice(player)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(player)
            tackle_skill = find_select_thing(choices, "tackle")
            runner.make_choice(tackle_skill)

            # Bot turn
            choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
            bot_skill = choices[0]  # Choose the first skill, which could be either tackle or fireball
            runner.make_choice(bot_skill)

            # Check if bot's active creature has fainted
            if main_game_scene.bot.active_creature.hp == 0:
                if all(creature.hp == 0 for creature in main_game_scene.bot.creatures):
                    break  # Bot has lost, end the battle
                choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
                swap_choice = choices[0]  # Only one choice available: swap to next creature
                runner.make_choice(swap_choice)

            # Check if player's active creature has fainted
            if player.active_creature.hp == 0:
                if all(creature.hp == 0 for creature in player.creatures):
                    break  # Player has lost, end the battle
                choices = runner.dequeue_wait_for_choice(player)
                swap_choice = choices[0]  # Only one choice available: swap to next creature
                runner.make_choice(swap_choice)

        # Assert that the battle has ended
        assert (all(creature.hp == 0 for creature in player.creatures) or 
                all(creature.hp == 0 for creature in main_game_scene.bot.creatures))

        # Scene transitions to MainMenuScene
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
