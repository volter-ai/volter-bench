from __future__ import annotations

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Collection
from mini_game_engine.engine.new_mydantic.mydantic import Field

class Skill(AbstractThing):
    category: str = "Skill"
    damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int 
    max_hp: int
    skills: Collection[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: Collection[Creature]
