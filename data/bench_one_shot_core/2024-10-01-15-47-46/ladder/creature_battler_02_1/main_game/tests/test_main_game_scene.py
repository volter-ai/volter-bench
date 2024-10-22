import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button


class TestApp(App):
    pass

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_game_scene_battle_ends_correctly(app, player):
    opponent = app.create_bot("basic_opponent")
    scene = MainGameScene(app, player)
    scene.opponent = opponent
    
    runner = ThreadedSceneRunner()
    runner.start_game(scene)
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    assert scene.player_creature.hp <= 0 or scene.opponent_creature.hp <= 0
    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

def test_main_game_scene_equal_speed_consistent_order(app, player):
    opponent = app.create_bot("basic_opponent")
    scene = MainGameScene(app, player)
    scene.opponent = opponent
    scene.player_creature.speed = 3
    scene.opponent_creature.speed = 3
    
    runner = ThreadedSceneRunner()
    runner.start_game(scene)
    
    initial_player_hp = scene.player_creature.hp
    initial_opponent_hp = scene.opponent_creature.hp
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    assert scene.player_creature.hp == initial_player_hp
    assert scene.opponent_creature.hp < initial_opponent_hp
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    assert scene.player_creature.hp < initial_player_hp
    assert scene.opponent_creature.hp < initial_opponent_hp - 3
    
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)
    
    assert scene.player_creature.hp <= 0 or scene.opponent_creature.hp <= 0
    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

class TestMainGameSceneRandom:
    @pytest.fixture
    def app(self):
        return TestApp()

    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    def test_main_game_scene(self, app, player):
        HumanListener.random_mode = True
        iterations = 10
        completed_iterations = 0

        for _ in range(iterations):
            scene = MainGameScene(app, player)
            try:
                while True:
                    scene.run()
            except RandomModeGracefulExit:
                completed_iterations += 1
            except AbstractApp._QuitWholeGame:
                completed_iterations += 1
            except Exception as e:
                pytest.fail(f"Unexpected exception: {e}")

        assert completed_iterations > 0, "No iterations completed successfully"
        print(f"Completed {completed_iterations} out of {iterations} iterations")
