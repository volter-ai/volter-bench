from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, skill, attacker, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
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
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
        second = self.opponent_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill
        
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), (second, first, second_skill)]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self.calculate_damage(skill, attacker, defender)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")
                
                if defender.hp == 0:
                    return

    def run(self):
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            opponent_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.player_creature.hp == 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp == 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
