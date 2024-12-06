from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        
    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def execute_turn(self, first_creature: Creature, second_creature: Creature, 
                    first_skill: Skill, second_skill: Skill, 
                    first_player: Player, second_player: Player):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(first_player, f"{first_creature.display_name} used {first_skill.display_name}!")
        self._show_text(first_player, f"Dealt {damage} damage!")
        
        # Check if battle ended
        if second_creature.hp <= 0:
            return first_player
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(second_player, f"{second_creature.display_name} used {second_skill.display_name}!")
        self._show_text(second_player, f"Dealt {damage} damage!")
        
        # Check if battle ended
        if first_creature.hp <= 0:
            return second_player
            
        return None

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot choice phase
            opponent_skill = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, self.opponent_creature, player_skill, opponent_skill, self.player, self.opponent)
            elif self.opponent_creature.speed > self.player_creature.speed:
                first = (self.opponent_creature, self.player_creature, opponent_skill, player_skill, self.opponent, self.player)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, self.opponent_creature, player_skill, opponent_skill, self.player, self.opponent)
                else:
                    first = (self.opponent_creature, self.player_creature, opponent_skill, player_skill, self.opponent, self.player)

            # Execute turn
            winner = self.execute_turn(*first)
            
            if winner:
                if winner == self.player:
                    self._show_text(self.player, "You won!")
                else:
                    self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return
