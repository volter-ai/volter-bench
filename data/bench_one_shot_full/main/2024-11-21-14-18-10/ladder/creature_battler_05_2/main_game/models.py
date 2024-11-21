from __future__ import annotations
from typing import List, Optional
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Collection

class Skill(AbstractThing):
    skill_type: str
    is_physical: bool
    base_damage: int
    category: str = "Skill"

class Creature(AbstractThing):
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    sp_attack: int 
    sp_defense: int
    speed: int
    skills: List[Skill]
    category: str = "Creature"

class Player(AbstractPlayer):
    creatures: List[Creature]
    active_creature: Optional[Creature] = None
    category: str = "Player"
