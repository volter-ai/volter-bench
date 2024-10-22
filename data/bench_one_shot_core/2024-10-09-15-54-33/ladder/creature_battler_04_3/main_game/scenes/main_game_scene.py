import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_turn = self._determine_first_turn()

    def __str__(self):
        current_creature = self.player_creature if self.current_turn == "player" else self.opponent_creature
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Current Turn: {self.current_turn.capitalize()}

Available Skills:
{self._format_skills(current_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def _determine_first_turn(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return "player"
        elif self.player_creature.speed < self.opponent_creature.speed:
            return "opponent"
        else:
            return random.choice(["player", "opponent"])

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            if self.current_turn == "player":
                attacker, defender = self.player_creature, self.opponent_creature
                choices = [Button(skill.display_name) for skill in attacker.skills]
                choice = self._wait_for_choice(self.player, choices)
                skill = next(s for s in attacker.skills if s.display_name == choice.display_name)
            else:
                attacker, defender = self.opponent_creature, self.player_creature
                choices = [Button(skill.display_name) for skill in attacker.skills]
                choice = self._wait_for_choice(self.opponent, choices)
                skill = next(s for s in attacker.skills if s.display_name == choice.display_name)

            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)

            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

            if defender.hp == 0:
                winner = self.player if defender == self.opponent_creature else self.opponent
                self._show_text(self.player, f"{winner.display_name} wins!")
                break

            self.current_turn = "opponent" if self.current_turn == "player" else "player"

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
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

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
