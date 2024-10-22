import pytest
import random
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import HumanListener
from unittest.mock import patch
from mini_game_engine.engine.lib import RandomModeGracefulExit
from mini_game_engine.engine.lib import SelectThing


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

    def test_main_game_scene_full_battle(self, app, human_player, bot_player):
        scene = MainGameScene(app, human_player)
        scene.bot = bot_player
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Initial battle setup
        assert human_player.active_creature.prototype_id == "bubwool"
        assert bot_player.active_creature.prototype_id == "scizard"

        battle_ended = False
        while not battle_ended:
            # Human player's turn
            choices = runner.dequeue_wait_for_choice(human_player)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(human_player)
            tackle_skill = find_select_thing(choices, "tackle")
            runner.make_choice(tackle_skill)

            # Bot player's turn
            choices = runner.dequeue_wait_for_choice(bot_player)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(bot_player)
            bot_skill = random.choice([choice for choice in choices if isinstance(choice, SelectThing) and isinstance(choice.thing, Skill)])
            runner.make_choice(bot_skill)

            # Check if any creature fainted
            if human_player.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(human_player)
                new_creature = next(choice for choice in choices if isinstance(choice, SelectThing) and isinstance(choice.thing, Creature))
                runner.make_choice(new_creature)
                human_player.active_creature = new_creature.thing

            if bot_player.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(bot_player)
                new_creature = next(choice for choice in choices if isinstance(choice, SelectThing) and isinstance(choice.thing, Creature))
                runner.make_choice(new_creature)
                bot_player.active_creature = new_creature.thing

            # Check if battle has ended
            human_creatures_alive = any(creature.hp > 0 for creature in human_player.creatures)
            bot_creatures_alive = any(creature.hp > 0 for creature in bot_player.creatures)

            if not human_creatures_alive or not bot_creatures_alive:
                scene_transition = runner.dequeue_transition_to_scene()
                assert scene_transition == "MainMenuScene"
                battle_ended = True

        # Determine winner
        human_lost = all(creature.hp == 0 for creature in human_player.creatures)
        bot_lost = all(creature.hp == 0 for creature in bot_player.creatures)

        assert human_lost != bot_lost, "One player should win and one should lose"

        if human_lost:
            assert any(creature.hp > 0 for creature in bot_player.creatures)
        else:
            assert any(creature.hp > 0 for creature in human_player.creatures)
