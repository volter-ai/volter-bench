from __future__ import annotations

from typing import List

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing
from mini_game_engine.modules.graph import T


class Skill(AbstractThing):
    category: str = "Skill"
    damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    hp: int
    max_hp: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature]

def create_from_game_database(game_thing_prototype_id: str, game_thing_class: type[T]) -> T:
    """Takes in a prototype_id and uses the content JSON files to bootstrap a hydrated game entity"""
    return game_thing_class.from_prototype_id(game_thing_prototype_id)
