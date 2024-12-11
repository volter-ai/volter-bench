from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures to max HP
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5
                
        return int(raw_damage * effectiveness)

    def execute_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player_creature, self.opponent_creature, player_skill)
            second = (self.opponent_creature, self.player_creature, opponent_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent_creature, self.player_creature, opponent_skill)
            second = (self.player_creature, self.opponent_creature, player_skill)
        else:
            if random.random() < 0.5:
                first = (self.player_creature, self.opponent_creature, player_skill)
                second = (self.opponent_creature, self.player_creature, opponent_skill)
            else:
                first = (self.opponent_creature, self.player_creature, opponent_skill)
                second = (self.player_creature, self.opponent_creature, player_skill)

        # Execute attacks in order
        for attacker, defender, skill in [first, second]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self.calculate_damage(attacker, defender, skill)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")
