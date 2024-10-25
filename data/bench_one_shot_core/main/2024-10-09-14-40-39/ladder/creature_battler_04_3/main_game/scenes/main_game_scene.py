from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_phase = "player_choice"
        self.queued_skills = {"player": None, "opponent": None}

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Current Phase: {self.current_phase.replace("_", " ").capitalize()}

Available Skills:
{self._format_skills(self.player_creature.skills if self.current_phase == "player_choice" else self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            if self.current_phase == "player_choice":
                self._player_choice_phase()
            elif self.current_phase == "foe_choice":
                self._foe_choice_phase()
            elif self.current_phase == "resolution":
                self._resolution_phase()

            if self.player_creature.hp == 0 or self.opponent_creature.hp == 0:
                winner = self.player if self.opponent_creature.hp == 0 else self.opponent
                self._show_text(self.player, f"{winner.display_name} wins!")
                break

        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        skill = next(s for s in self.player_creature.skills if s.display_name == choice.display_name)
        self.queued_skills["player"] = skill
        self.current_phase = "foe_choice"

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        skill = next(s for s in self.opponent_creature.skills if s.display_name == choice.display_name)
        self.queued_skills["opponent"] = skill
        self.current_phase = "resolution"

    def _resolution_phase(self):
        first, second = self._determine_turn_order()
        self._execute_skill(first)
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._execute_skill(second)
        self.queued_skills = {"player": None, "opponent": None}
        self.current_phase = "player_choice"

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return ("player", self.player_creature), ("opponent", self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return ("opponent", self.opponent_creature), ("player", self.player_creature)
        else:
            return random.sample([("player", self.player_creature), ("opponent", self.opponent_creature)], 2)

    def _execute_skill(self, turn_info):
        side, attacker = turn_info
        defender = self.opponent_creature if side == "player" else self.player_creature
        skill = self.queued_skills[side]

        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = round(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2.0
            elif defender_type == "water":
                return 0.5
        elif skill_type == "water":
            if defender_type == "fire":
                return 2.0
            elif defender_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2.0
            elif defender_type == "fire":
                return 0.5
        return 1.0
