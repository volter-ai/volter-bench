import uuid
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener, create_from_game_database
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player, Creature


class App(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player_data = Player.get_data().get("prototypes")["default_player"]
        player = Player(
            uid=player_id,
            display_name=player_data["display_name"],
            description=player_data["description"],
            prototype_id="default_player",
            creatures=[self.create_creature(creature_id) for creature_id in player_data["creatures"]]
        )
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str):
        bot_data = Player.get_data().get("prototypes")[prototype_id]
        bot = Player(
            uid=str(uuid.uuid4()),
            display_name=bot_data["display_name"],
            description=bot_data["description"],
            prototype_id=prototype_id,
            creatures=[self.create_creature(creature_id) for creature_id in bot_data["creatures"]]
        )
        bot.set_listener(BotListener())
        return bot

    def create_creature(self, creature_id: str):
        return create_from_game_database(creature_id, Creature)

if __name__ == '__main__':
    app = App()
    app.run(app.create_player("just_a_guy"))
