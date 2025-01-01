from __future__ import annotations
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing
from typing import List

class Skill(AbstractThing):
    base_damage: int

class Creature(AbstractThing):
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: List[Skill]

class Player(AbstractPlayer):
    creatures: List[Creature]
