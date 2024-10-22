import pytest
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Creature
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
    def human_player(self, app):
        player = app.create_player("human_player")
        player.creatures = [
            Creature.from_prototype_id("bubwool"),
            Creature.from_prototype_id("dumbird")
        ]
        player.active_creature = player.creatures[0]
        return player

    @pytest.fixture
    def bot_player(self, app):
        bot = app.create_bot("basic_opponent")
        bot.creatures = [
            Creature.from_prototype_id("scizard"),
            Creature.from_prototype_id("dumbird")
        ]
        bot.active_creature = bot.creatures[0]
        return bot

    def test_main_game_scene_playthrough(self, app, human_player, bot_player):
        scene = MainGameScene(app, human_player)
        scene.bot = bot_player
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        while True:
            # Human player's turn
            choices = runner.dequeue_wait_for_choice(human_player)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            skill_choices = runner.dequeue_wait_for_choice(human_player)
            tackle_choice = find_select_thing(skill_choices, "tackle")
            runner.make_choice(tackle_choice)

            # Bot player's turn
            choices = runner.dequeue_wait_for_choice(bot_player)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            skill_choices = runner.dequeue_wait_for_choice(bot_player)
            tackle_choice = find_select_thing(skill_choices, "tackle")
            runner.make_choice(tackle_choice)

            # Check if any creature has fainted
            if human_player.active_creature.hp == 0:
                if all(creature.hp == 0 for creature in human_player.creatures):
                    break
                choices = runner.dequeue_wait_for_choice(human_player)
                new_creature = choices[0]
                runner.make_choice(new_creature)

            if bot_player.active_creature.hp == 0:
                if all(creature.hp == 0 for creature in bot_player.creatures):
                    break
                choices = runner.dequeue_wait_for_choice(bot_player)
                new_creature = choices[0]
                runner.make_choice(new_creature)

        # Expect the battle to end
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

        # Additional assertions to verify the battle outcome
        assert all(creature.hp == 0 for creature in human_player.creatures) or all(creature.hp == 0 for creature in bot_player.creatures)
        assert not (all(creature.hp == 0 for creature in human_player.creatures) and all(creature.hp == 0 for creature in bot_player.creatures))
