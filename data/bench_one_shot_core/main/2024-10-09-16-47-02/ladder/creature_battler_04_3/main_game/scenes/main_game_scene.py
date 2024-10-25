from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                break

        self._show_battle_result()
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = self.player_creature, self.opponent_creature
            first_skill, second_skill = player_skill, foe_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = self.opponent_creature, self.player_creature
            first_skill, second_skill = foe_skill, player_skill
        else:
            # Random order for equal speeds
            if random.choice([True, False]):
                first, second = self.player_creature, self.opponent_creature
                first_skill, second_skill = player_skill, foe_skill
            else:
                first, second = self.opponent_creature, self.player_creature
                first_skill, second_skill = foe_skill, player_skill

        self._execute_skill(first, second, first_skill)
        if second.hp > 0:
            self._execute_skill(second, first, second_skill)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def _calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "normal": {},  # Normal type is neither effective nor ineffective against any type
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

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
