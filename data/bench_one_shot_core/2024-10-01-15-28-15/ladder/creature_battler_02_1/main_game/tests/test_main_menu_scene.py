import pytest
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import AbstractApp, BotListener, HumanListener


class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene)
        self.register_scene("MainGameScene", MainGameScene)
        self.transition_count = 0
        self.max_transitions = 10

    def create_player(self, player_id: str) -> Player:
        player = Player.from_prototype_id("default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str) -> Player:
        bot = Player.from_prototype_id(prototype_id)
        bot.set_listener(BotListener())
        return bot

    def transition_to_scene(self, scene_name: str, **kwargs):
        self.transition_count += 1
        if self.transition_count > self.max_transitions:
            self.quit_whole_game()
        super().transition_to_scene(scene_name, **kwargs)

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_menu_scene(app, player):
    HumanListener.random_mode = True
    scene = MainMenuScene(app, player)
    try:
        scene.run()
    except AbstractApp._QuitWholeGame:
        pass  # This is the expected behavior when quitting the game
    assert app.transition_count > 0, "The game should have transitioned at least once"
    assert app.transition_count <= app.max_transitions, f"The game should not have transitioned more than {app.max_transitions} times"
