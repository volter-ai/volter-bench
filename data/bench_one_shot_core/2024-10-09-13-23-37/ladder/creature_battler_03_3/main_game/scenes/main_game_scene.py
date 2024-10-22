import math
import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
Your skills: {', '.join([skill.display_name for skill in self.player_creature.skills])}

{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})
Opponent's skills: {', '.join([skill.display_name for skill in self.opponent_creature.skills])}

Your turn! Choose a skill:
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
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

        # Reset creatures' HP after the battle
        self.reset_creatures()
        
        # After the battle ends, transition back to the main menu
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed == self.opponent_creature.speed:
            # Randomly decide who goes first when speeds are equal
            first_attacker, second_attacker = random.sample([self.player_creature, self.opponent_creature], 2)
            first_skill = player_skill if first_attacker == self.player_creature else opponent_skill
            second_skill = opponent_skill if first_attacker == self.player_creature else player_skill
        elif self.player_creature.speed > self.opponent_creature.speed:
            first_attacker, second_attacker = self.player_creature, self.opponent_creature
            first_skill, second_skill = player_skill, opponent_skill
        else:
            first_attacker, second_attacker = self.opponent_creature, self.player_creature
            first_skill, second_skill = opponent_skill, player_skill

        self.execute_skill(first_attacker, second_attacker, first_skill)
        if second_attacker.hp > 0:
            self.execute_skill(second_attacker, first_attacker, second_skill)

    def execute_skill(self, attacker, defender, skill):
        raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(math.floor(raw_damage * weakness_factor))
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal" or defender_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5, "fire": 1.0},
            "water": {"fire": 2.0, "leaf": 0.5, "water": 1.0},
            "leaf": {"water": 2.0, "fire": 0.5, "leaf": 1.0}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
