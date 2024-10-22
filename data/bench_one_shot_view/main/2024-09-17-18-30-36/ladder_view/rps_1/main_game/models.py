from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field


class Skill(AbstractThing):
    category: str = "Skill"

class Player(AbstractPlayer):
    category: str = "Player"
    skills: list[Skill] = Field(default_factory=list)
