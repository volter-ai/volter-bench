from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer
from typing import List


class Skill(AbstractThing):
    category: str = "Skill"
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature]
