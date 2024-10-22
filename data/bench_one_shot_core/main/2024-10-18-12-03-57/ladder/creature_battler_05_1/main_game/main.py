import uuid
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        
        # Set the active_creature to the first creature in the list
        if player.creatures:
            player.active_creature = player.creatures[0]
        
        return player

    def create_bot(self, prototype_id: str):
        bot = Player.from_prototype_id(prototype_id=prototype_id)
        bot.uid = str(uuid.uuid4())
        bot.set_listener(BotListener())
        
        # Set the active_creature to the first creature in the list
        if bot.creatures:
            bot.active_creature = bot.creatures[0]
        
        return bot

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
