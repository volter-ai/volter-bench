from __future__ import annotations

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Collection

class Skill(AbstractThing):
    damage: int
    category: str = "Skill"

class Creature(AbstractThing):
    hp: int 
    max_hp: int
    skills: Collection[Skill]
    category: str = "Creature"

class Player(AbstractPlayer):
    creatures: Collection[Creature]
    category: str = "Player"
