from __future__ import annotations
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, create_from_game_database
from typing import List

class Skill(AbstractThing):
    display_name: str
    skill_type: str
    base_damage: int
    description: str

class Creature(AbstractThing):
    display_name: str
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: List[Skill]

class Player(AbstractPlayer):
    display_name: str
    creatures: List[Creature]
