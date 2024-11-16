from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        # Normal type has no strengths or weaknesses
        if skill_type == "normal":
            return 1.0
            
        # Type effectiveness matrix
        effectiveness = {
            "fire": {
                "leaf": 2.0,    # Fire strong vs Leaf
                "water": 0.5,   # Fire weak vs Water
                "fire": 1.0     # Same type normal damage
            },
            "water": {
                "fire": 2.0,    # Water strong vs Fire
                "leaf": 0.5,    # Water weak vs Leaf
                "water": 1.0    # Same type normal damage
            },
            "leaf": {
                "water": 2.0,   # Leaf strong vs Water
                "fire": 0.5,    # Leaf weak vs Fire
                "leaf": 1.0     # Same type normal damage
            }
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage exactly as specified
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Get type multiplier
        type_multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage with type effectiveness
        final_damage = int(type_multiplier * raw_damage)
        
        # Damage can't be negative
        return max(0, final_damage)

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        
        effectiveness = "It's super effective!" if self.get_type_multiplier(first_skill.skill_type, second_creature.creature_type) > 1 else \
                       "It's not very effective..." if self.get_type_multiplier(first_skill.skill_type, second_creature.creature_type) < 1 else ""
        
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage! {effectiveness}")
        
        # Second attack if target still alive
        if second_creature.hp > 0:
            damage = self.calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp -= damage
            
            effectiveness = "It's super effective!" if self.get_type_multiplier(second_skill.skill_type, first_creature.creature_type) > 1 else \
                           "It's not very effective..." if self.get_type_multiplier(second_skill.skill_type, first_creature.creature_type) < 1 else ""
            
            self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage! {effectiveness}")

    def run(self):
        while True:
            # Player choice phase
            player_skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, player_skill_choices).thing

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
            self.execute_turn(first[0], second[0], first[1], second[1])

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._quit_whole_game()
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._quit_whole_game()
