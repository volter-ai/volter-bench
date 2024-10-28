from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List, Optional


class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str
    is_physical: bool
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    skills: List[Skill] = Field(default_factory=list)

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature] = Field(default_factory=list)
    active_creature: Optional[Creature] = Field(default=None)
