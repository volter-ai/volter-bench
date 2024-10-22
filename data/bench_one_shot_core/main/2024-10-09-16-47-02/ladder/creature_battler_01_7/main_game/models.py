from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer
from typing import List


class Skill(AbstractThing):
    damage: int
    category: str = "Skill"

class Creature(AbstractThing):
    hp: int
    max_hp: int
    skills: List[Skill]
    category: str = "Creature"

class Player(AbstractPlayer):
    creatures: List[Creature]
    category: str = "Player"
