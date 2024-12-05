from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
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
        first = self.player
        second = self.opponent
        first_skill = player_skill
        second_skill = opponent_skill
        
        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), (second, first, second_skill)]:
            if attacker == self.player:
                atk_creature = self.player_creature
                def_creature = self.opponent_creature
            else:
                atk_creature = self.opponent_creature
                def_creature = self.player_creature
                
            damage = self.calculate_damage(skill, atk_creature, def_creature)
            def_creature.hp = max(0, def_creature.hp - damage)
            
            self._show_text(self.player, f"{atk_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")
            
            if def_creature.hp <= 0:
                return True
                
        return False

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")
        
        while True:
            # Player choice phase
            player_skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_skill_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)
            
            # Opponent choice phase
            opponent_skill_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            opponent_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)
            
            # Resolution phase
            battle_ended = self.execute_turn(player_skill, opponent_skill)
            
            if battle_ended:
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
