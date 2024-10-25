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
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                self.battle_ended = True

        self._reset_creatures()
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
            return [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
        elif self.player_creature.speed < self.opponent_creature.speed:
            return [(self.opponent.prototype_id, self.opponent_creature), (self.player.prototype_id, self.player_creature)]
        else:
            # Random decision when speeds are equal
            if random.choice([True, False]):
                return [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
            else:
                return [(self.opponent.prototype_id, self.opponent_creature), (self.player.prototype_id, self.player_creature)]

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        execution_order = self._determine_execution_order()
        skills = {self.player.prototype_id: player_skill, self.opponent.prototype_id: foe_skill}

        for attacker_id, attacker_creature in execution_order:
            attacker = self.player if attacker_id == self.player.prototype_id else self.opponent
            defender = self.opponent if attacker == self.player else self.player
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            skill = skills[attacker_id]

            self._execute_skill(attacker, attacker_creature, skill, defender_creature)
            if defender_creature.hp <= 0:
                break

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = self._calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, skill: Skill, defender: Creature) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _transition_to_main_menu(self):
        self._transition_to_scene("MainMenuScene")
