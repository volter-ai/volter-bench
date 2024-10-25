from __future__ import annotations
from mini_game_engine.engine.lib import AbstractThing, AbstractPlayer, Field
from typing import List
from mini_game_engine.engine.lib import T


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
    creatures: List[Creature]
    active_creature: Creature = Field(default=None)

def create_from_game_database(game_thing_prototype_id: str, game_thing_class: type[T]) -> T:
    """Takes in a prototype_id and uses the content JSON files to bootstrap a hydrated game entity"""
    return game_thing_class.from_prototype_id(game_thing_prototype_id)
