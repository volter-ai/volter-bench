from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List


class Skill(AbstractThing):
    category: str = "Skill"
    damage: int
    description: str

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int
    max_hp: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature] = Field(default_factory=list)
