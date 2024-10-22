from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List


class Skill(AbstractThing):
    category: str = "Skill"
    base_damage: int = Field(...)

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int = Field(...)
    max_hp: int = Field(...)
    attack: int = Field(...)
    defense: int = Field(...)
    speed: int = Field(...)
    skills: List[Skill] = Field(...)

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature] = Field(...)
