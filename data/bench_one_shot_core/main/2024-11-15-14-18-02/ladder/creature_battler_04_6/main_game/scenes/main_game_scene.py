from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Calculate type multiplier
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
            if defender.hp <= 0:
                continue
                
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp -= damage
            
            self._show_text(self.player, 
                f"{attacker.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.display_name}!")

    def run(self):
        while True:
            # Player turn
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_choice.display_name)
            
            # Opponent turn
            opponent_choice = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            opponent_skill = next(s for s in self.opponent_creature.skills 
                                if s.display_name == opponent_choice.display_name)
            
            # Execute turn
            self.execute_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
        
        self._transition_to_scene("MainMenuScene")
