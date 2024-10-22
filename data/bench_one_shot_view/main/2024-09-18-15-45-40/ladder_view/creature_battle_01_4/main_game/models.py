from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer


class Skill(AbstractThing):
    category: str = "Skill"
    damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int
    max_hp: int
    skills: list[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: list[Creature]
