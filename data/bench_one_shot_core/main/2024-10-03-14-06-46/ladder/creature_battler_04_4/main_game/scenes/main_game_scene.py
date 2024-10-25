from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_turn = "player"

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Current Turn: {self.current_turn.capitalize()}

Available Skills:
{self._format_skills()}
"""

    def _format_skills(self):
        if self.current_turn == "player":
            creature = self.player_creature
        else:
            creature = self.opponent_creature
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()
            
            self._resolve_skills(player_skill, opponent_skill)
            
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent_creature.display_name} chose {skill.display_name}!")
        return skill

    def _resolve_skills(self, player_skill: Skill, opponent_skill: Skill):
        first, second = self._determine_skill_order(self.player_creature, self.opponent_creature)
        
        if first == self.player_creature:
            self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if not self._check_battle_end():
                self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        else:
            self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if not self._check_battle_end():
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)

    def _determine_skill_order(self, creature1: Creature, creature2: Creature):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you won the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
