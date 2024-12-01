from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from main_game.models import Skill, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate base damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def execute_turn(self, first: tuple[Creature, Skill], second: tuple[Creature, Skill]):
        for attacker, skill in [first, second]:
            if attacker == self.player_creature:
                defender = self.opponent_creature
                atk_name = self.player.display_name
                def_name = self.opponent.display_name
            else:
                defender = self.player_creature
                atk_name = self.opponent.display_name
                def_name = self.player.display_name

            damage = self.calculate_damage(skill, attacker, defender)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, 
                f"{atk_name}'s {attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player,
                f"It dealt {damage} damage to {def_name}'s {defender.display_name}!")
            
            if defender.hp <= 0:
                return True
        return False

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            
            # Opponent choice phase  
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            
            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, player_skill)
                second = (self.opponent_creature, opponent_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, opponent_skill)
                second = (self.player_creature, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, player_skill)
                    second = (self.opponent_creature, opponent_skill)
                else:
                    first = (self.opponent_creature, opponent_skill)
                    second = (self.player_creature, player_skill)
            
            # Execute turn
            battle_ended = self.execute_turn(first, second)
            
            if battle_ended:
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
