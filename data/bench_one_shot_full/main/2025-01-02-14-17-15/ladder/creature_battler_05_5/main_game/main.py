import uuid
from mini_game_engine.engine.lib import HumanListener, AbstractApp, BotListener
from main_game.models import Player, Creature

class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        player.active_creature = player.creatures[0]  # Set the first creature as the active creature
        return player

    def create_bot(self, prototype_id: str):
        bot = Player.from_prototype_id(prototype_id=prototype_id)
        bot.uid = str(uuid.uuid4())
        bot.set_listener(BotListener())
        bot.active_creature = bot.creatures[0]  # Set the first creature as the active creature
        return bot

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
