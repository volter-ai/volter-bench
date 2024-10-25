from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "Battle start!")
        while not self.battle_ended:
            self._player_choice_phase()
            if not self.battle_ended:
                self._foe_choice_phase()
            if not self.battle_ended:
                self._resolution_phase()

    def _player_choice_phase(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def _foe_choice_phase(self):
        self._show_text(self.opponent, "Opponent's turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing

    def _resolution_phase(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
            if not self.battle_ended:
                self._execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
            if not self.battle_ended:
                self._execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
        else:
            # Speed tie, randomly decide who goes first
            if random.choice([True, False]):
                self._execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)
                if not self.battle_ended:
                    self._execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
                if not self.battle_ended:
                    self._execute_skill(self.player, self.player_creature, self.player_skill, self.opponent_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        raw_damage = float(attacker_creature.attack + skill.base_damage - defender_creature.defense)
        factor = self._get_weakness_resistance_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")
        self._check_battle_end()

    def _get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self.battle_ended = True
            self._show_text(self.player, "Returning to main menu...")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self.battle_ended = True
            self._show_text(self.player, "Returning to main menu...")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
