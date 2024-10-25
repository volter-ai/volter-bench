from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while not self.battle_ended:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            self.check_battle_end()

        self.reset_creatures()
        self.return_to_main_menu()

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
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Speeds are equal, randomly decide who goes first
            first_attacker, first_creature, first_skill, second_attacker, second_creature, second_skill = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, opponent_skill),
                (self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature, player_skill)
            ])
            
            self.execute_skill(first_attacker, first_creature, first_skill, second_creature)
            if second_creature.hp > 0:
                self.execute_skill(second_attacker, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

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
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
            self.battle_ended = True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You won the battle!")
            self.battle_ended = True
        return self.battle_ended

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def return_to_main_menu(self):
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
