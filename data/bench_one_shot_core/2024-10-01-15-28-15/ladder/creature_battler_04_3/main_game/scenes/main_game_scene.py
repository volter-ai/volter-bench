import random
from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Opponent: {self.opponent.display_name}\n"
            f"Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})\n"
        )

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            
            self._resolution_phase(player_skill, opponent_skill)
            
            if self._check_battle_end():
                break

        self._reset_creature_state()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            creatures = [self.player_creature, self.opponent_creature]
            skills = [player_skill, opponent_skill]
            random.shuffle(list(zip(creatures, skills)))
            for creature, skill in zip(creatures, skills):
                if creature == self.player_creature:
                    self._execute_skill(self.player, self.player_creature, skill, self.opponent_creature)
                else:
                    self._execute_skill(self.opponent, self.opponent_creature, skill, self.player_creature)
                if self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0:
                    break

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        if skill.is_physical:
            raw_damage = float(attacker_creature.attack + skill.base_damage - defender_creature.defense)
        else:
            raw_damage = float(attacker_creature.sp_attack) / float(defender_creature.sp_defense) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creature_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
