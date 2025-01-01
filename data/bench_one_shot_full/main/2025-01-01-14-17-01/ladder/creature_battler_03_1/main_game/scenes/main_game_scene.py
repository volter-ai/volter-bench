from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Main Game===
Player Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp})
Opponent Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp})
Choose a skill:
{self._list_skills(self.player_creature.skills)}
"""

    def _list_skills(self, skills):
        return "\n".join([f"{i+1}. {skill.display_name} ({skill.skill_type})" for i, skill in enumerate(skills)])

    def run(self):
        while self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._player_choice_phase()
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You win!")
                self._quit_whole_game()
                return
            self._foe_choice_phase()
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lose!")
                self._quit_whole_game()
                return

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = self.player_creature.skills[choices.index(choice)]
        self._resolve_turn(selected_skill)

    def _foe_choice_phase(self):
        selected_skill = random.choice(self.opponent_creature.skills)
        self._resolve_turn(selected_skill, foe_turn=True)

    def _resolve_turn(self, player_skill: Skill, foe_turn=False):
        if foe_turn:
            foe_skill = player_skill
            player_skill = random.choice(self.player_creature.skills)
        else:
            foe_skill = random.choice(self.opponent_creature.skills)

        if self.player_creature.speed > self.opponent_creature.speed:
            self._resolve_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self._resolve_skill(self.opponent_creature, self.player_creature, foe_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._resolve_skill(self.opponent_creature, self.player_creature, foe_skill)
            if self.player_creature.hp > 0:
                self._resolve_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            if random.choice([True, False]):
                self._resolve_skill(self.player_creature, self.opponent_creature, player_skill)
                if self.opponent_creature.hp > 0:
                    self._resolve_skill(self.opponent_creature, self.player_creature, foe_skill)
            else:
                self._resolve_skill(self.opponent_creature, self.player_creature, foe_skill)
                if self.player_creature.hp > 0:
                    self._resolve_skill(self.player_creature, self.opponent_creature, player_skill)

    def _resolve_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_resistance_factor = self._calculate_weakness_resistance(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * weakness_resistance_factor)
        defender.hp = max(defender.hp - final_damage, 0)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def _calculate_weakness_resistance(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)
