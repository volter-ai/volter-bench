from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # If speeds are equal, randomly choose who goes first
            first_attacker, first_defender, first_skill, second_attacker, second_defender, second_skill = random.choice([
                (self.player_creature, self.opponent_creature, player_skill, self.opponent_creature, self.player_creature, opponent_skill),
                (self.opponent_creature, self.player_creature, opponent_skill, self.player_creature, self.opponent_creature, player_skill)
            ])
            
            self.execute_skill(first_attacker, first_defender, first_skill)
            if first_defender.hp > 0:
                self.execute_skill(second_attacker, second_defender, second_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage to {defender.display_name}.")

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire" and defender_type == "leaf":
            return 2.0
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "fire":
            return 2.0
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "water":
            return 2.0
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1.0

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted. You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
