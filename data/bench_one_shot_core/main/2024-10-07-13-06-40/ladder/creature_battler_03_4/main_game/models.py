from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer


class Skill(AbstractThing):
    skill_type: str
    base_damage: int

class Creature(AbstractThing):
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: list[Skill]

class Player(AbstractPlayer):
    creatures: list[Creature]
