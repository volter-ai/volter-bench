from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List


class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    display_name: str
    creatures: List[Creature] = Field(default_factory=list)
