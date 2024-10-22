from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        return self._player_choice_phase(opponent, creature)

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        
        self._execute_skill(first[0], first[1], second[1])
        if not self._check_battle_end():
            self._execute_skill(second[0], second[1], first[1])

    def _determine_order(self, creature1: Creature, creature2: Creature):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, self.player_creature), (self.opponent, creature2, self.opponent_creature)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, self.opponent_creature), (self.player, creature1, self.player_creature)
        else:
            if random.choice([True, False]):
                return (self.player, creature1, self.player_creature), (self.opponent, creature2, self.opponent_creature)
            else:
                return (self.opponent, creature2, self.opponent_creature), (self.player, creature1, self.player_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature):
        skill = self._player_choice_phase(attacker, attacker_creature)
        damage = self._calculate_damage(skill, attacker_creature, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
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
