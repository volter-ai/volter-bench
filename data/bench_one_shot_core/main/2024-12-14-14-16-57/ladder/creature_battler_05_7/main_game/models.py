from __future__ import annotations
from typing import List, Optional
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Collection

class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str  # normal, fire, water, leaf
    is_physical: bool
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str  # normal, fire, water, leaf
    hp: int
    max_hp: int 
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    skills: Collection[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: Collection[Creature]
    active_creature: Optional[Creature] = None
