from __future__ import annotations
from typing import List
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field


class Skill(AbstractThing):
    category: str = "Skill"
    damage: int = Field(default=0)

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int = Field(default=0)
    max_hp: int = Field(default=0)
    skills: List[Skill] = Field(default_factory=list)

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature] = Field(default_factory=list)
