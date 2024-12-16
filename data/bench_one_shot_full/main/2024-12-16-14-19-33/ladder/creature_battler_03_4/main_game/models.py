from __future__ import annotations
from typing import List
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Collection

class Skill(AbstractThing):
    base_damage: int
    skill_type: str
    category: str = "Skill"

class Creature(AbstractThing):
    creature_type: str
    hp: int
    max_hp: int 
    attack: int
    defense: int
    speed: int
    skills: List[Skill]
    category: str = "Creature"

class Player(AbstractPlayer):
    creatures: List[Creature]
    category: str = "Player"
