from __future__ import annotations
from typing import List
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Collection

class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str  # normal, fire, water, leaf
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str  # normal, fire, water, leaf
    hp: int
    max_hp: int 
    attack: int
    defense: int
    speed: int
    skills: Collection[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: Collection[Creature]
