from __future__ import annotations

from typing import List

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Field


class Skill(AbstractThing):
    skill_type: str
    is_physical: bool
    base_damage: int

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

class Player(AbstractPlayer):
    creatures: List[Creature] = Field(default_factory=list)
