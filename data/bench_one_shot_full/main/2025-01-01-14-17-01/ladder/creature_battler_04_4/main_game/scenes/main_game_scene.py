from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.initial_player_creature_state = self._capture_creature_state(self.player_creature)

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name} | Creature: {self.player_creature.display_name} | HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent: {self.opponent.display_name} | Creature: {self.opponent_creature.display_name} | HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Choose a skill:
"""

    def run(self):
        try:
            while self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
                player_choice = self.player_turn()
                opponent_choice = self.opponent_turn()
                self.resolve_turn(player_choice, opponent_choice)
                if self.opponent_creature.hp <= 0:
                    self._show_text(self.player, "You win!")
                    break
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lose!")
                    break
        finally:
            self._reset_creature_state(self.player_creature, self.initial_player_creature_state)
            self._quit_whole_game()

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        # Determine turn order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # Random tie-breaking
            if random.choice([True, False]):
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
                if self.opponent_creature.hp > 0:
                    self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            else:
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
                if self.player_creature.hp > 0:
                    self.execute_skill(self.player_creature, self.opponent_creature, player_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(defender.hp - raw_damage, 0)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {raw_damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        return int(raw_damage * self.type_effectiveness(skill.skill_type, defender.creature_type))

    def type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def _capture_creature_state(self, creature: Creature) -> dict:
        return {
            "hp": creature.hp,
            "max_hp": creature.max_hp,
            "attack": creature.attack,
            "defense": creature.defense,
            "sp_attack": creature.sp_attack,
            "sp_defense": creature.sp_defense,
            "speed": creature.speed
        }

    def _reset_creature_state(self, creature: Creature, state: dict):
        creature.hp = state["hp"]
        creature.max_hp = state["max_hp"]
        creature.attack = state["attack"]
        creature.defense = state["defense"]
        creature.sp_attack = state["sp_attack"]
        creature.sp_defense = state["sp_defense"]
        creature.speed = state["speed"]
