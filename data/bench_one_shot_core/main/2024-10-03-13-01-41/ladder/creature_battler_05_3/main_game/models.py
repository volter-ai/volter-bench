from __future__ import annotations
from typing import List, Optional
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field


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
    skills: List[str]  # List of skill prototype_ids

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[str] = Field(default_factory=list)  # List of creature prototype_ids
    active_creature: Optional[str] = None  # Optional creature prototype_id
