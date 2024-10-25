from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
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

Available Skills:
{self._format_skills(self.player_creature)}
"""

    def _format_skills(self, creature):
        return "\n".join([f"- {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")
        
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()
            
            self._resolve_turn(
                (self.player_creature, player_skill),
                (self.opponent_creature, opponent_skill)
            )
            
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_action, opponent_action):
        player_creature, player_skill = player_action
        opponent_creature, opponent_skill = opponent_action

        if player_creature.speed > opponent_creature.speed:
            first, second = player_action, opponent_action
        elif player_creature.speed < opponent_creature.speed:
            first, second = opponent_action, player_action
        else:
            if random.choice([True, False]):
                first, second = player_action, opponent_action
            else:
                first, second = opponent_action, player_action

        self._resolve_skill(*first)
        if not self._check_battle_end():
            self._resolve_skill(*second)

    def _resolve_skill(self, attacker: Creature, skill: Skill):
        if attacker == self.player_creature:
            defender = self.opponent_creature
        else:
            defender = self.player_creature

        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            if defender.sp_defense == 0:
                raw_damage = skill.base_damage  # Avoid division by zero
            else:
                raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(round(weakness_factor * raw_damage))
        
        defender.hp = max(0, defender.hp - final_damage)
        
        message = f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage to {defender.display_name}."
        self._show_text(self.player, message)
        self._show_text(self.opponent, message)

    def _calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0  # Normal type is neither effective nor ineffective against any type
        
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0 and self.opponent_creature.hp <= 0:
            self._show_text(self.player, "The battle ended in a tie!")
            self._show_text(self.opponent, "The battle ended in a tie!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
