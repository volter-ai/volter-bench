from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while not self.battle_ended:
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                self.battle_ended = True
                self._show_battle_result()
                self._transition_to_main_menu()

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_execution_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return [(self.player, self.player_creature), (self.opponent, self.opponent_creature)]
        elif self.player_creature.speed < self.opponent_creature.speed:
            return [(self.opponent, self.opponent_creature), (self.player, self.player_creature)]
        else:
            order = [(self.player, self.player_creature), (self.opponent, self.opponent_creature)]
            random.shuffle(order)
            return order

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        execution_order = self._determine_execution_order()
        skills = {self.player.uid: player_skill, self.opponent.uid: foe_skill}

        for attacker, attacker_creature in execution_order:
            defender, defender_creature = next((p, c) for p, c in execution_order if p != attacker)
            self._execute_skill(attacker, attacker_creature, skills[attacker.uid], defender_creature)
            if defender_creature.hp <= 0:
                break

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self) -> bool:
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _show_battle_result(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _transition_to_main_menu(self):
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
