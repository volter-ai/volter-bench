from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player
import uuid


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str):
        bot = Player.from_prototype_id(prototype_id=prototype_id)
        bot.uid = str(uuid.uuid4())
        bot.set_listener(BotListener())
        return bot

    def transition_to_scene(self, scene_id: str, **kwargs):
        if scene_id == "MainMenuScene":
            self.reset_creatures(kwargs.get('player'))
        super().transition_to_scene(scene_id, **kwargs)

    def reset_creatures(self, player):
        for creature in player.creatures:
            creature.hp = creature.max_hp
        if hasattr(self, 'opponent'):
            for creature in self.opponent.creatures:
                creature.hp = creature.max_hp

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
