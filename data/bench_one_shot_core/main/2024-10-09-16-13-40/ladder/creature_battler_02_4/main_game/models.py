from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List


class Skill(AbstractThing):
    base_damage: int = 0

class Creature(AbstractThing):
    hp: int = 0
    max_hp: int = 0
    attack: int = 0
    defense: int = 0
    speed: int = 0
    skills: List[Skill] = Field(default_factory=list)

class Player(AbstractPlayer):
    creatures: List[Creature] = Field(default_factory=list)
