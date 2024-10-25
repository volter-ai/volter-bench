from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, create_from_game_database
# New game entities should extend AbstractThing

class Player(AbstractPlayer):
    category: str = "Player"

