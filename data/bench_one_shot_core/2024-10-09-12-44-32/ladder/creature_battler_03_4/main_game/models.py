from __future__ import annotations

from typing import List

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing


class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str
    base_damage: float

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str
    hp: float
    max_hp: float
    attack: float
    defense: float
    speed: float
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature]
