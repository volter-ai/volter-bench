from __future__ import annotations
from typing import List
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Collection

class Skill(AbstractThing):
    skill_type: str
    base_damage: int

class Creature(AbstractThing):
    creature_type: str
    hp: int 
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: Collection[Skill]

class Player(AbstractPlayer):
    creatures: Collection[Creature]
