from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_phase = "player_choice"
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Current Phase: {self.current_phase}

Player Skills:
{self._format_skills(self.player_creature.skills)}

Opponent Skills:
{self._format_skills(self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while not self.battle_ended:
            if self.current_phase == "player_choice":
                self._player_choice_phase()
            elif self.current_phase == "foe_choice":
                self._foe_choice_phase()
            elif self.current_phase == "resolution":
                self._resolution_phase()

            if self._check_battle_end():
                self.battle_ended = True

        # Transition back to the main menu after the battle ends
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing
        self.current_phase = "foe_choice"

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing
        self.current_phase = "resolution"

    def _resolution_phase(self):
        first, second = self._determine_order()
        self._execute_skill(first[1], first[2], second[2])
        if not self._check_battle_end():
            self._execute_skill(second[1], second[2], first[2])
        self.current_phase = "player_choice"

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_skill, self.player_creature), (self.opponent, self.opponent_skill, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_skill, self.opponent_creature), (self.player, self.player_skill, self.player_creature)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_skill, self.player_creature), (self.opponent, self.opponent_skill, self.opponent_creature)
            else:
                return (self.opponent, self.opponent_skill, self.opponent_creature), (self.player, self.player_skill, self.player_creature)

    def _execute_skill(self, skill: Skill, attacker_creature: Creature, defender_creature: Creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def _calculate_weakness_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False
