from mini_game_engine.engine.lib import AbstractGameScene, Button
import random
import math

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}  # Will store {player_uid: skill}

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player phase
            self.player_phase()
            
            # Opponent phase  
            self.opponent_phase()
            
            # Resolution phase
            self.resolution_phase()
            
            # Check win condition
            if self.check_battle_end():
                break

        # Reset creatures
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = next(s for s in self.player_creature.skills 
                            if s.display_name == choice.display_name)
        self.queued_skills[self.player.uid] = selected_skill

    def opponent_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        selected_skill = next(s for s in self.opponent_creature.skills 
                            if s.display_name == choice.display_name)
        self.queued_skills[self.opponent.uid] = selected_skill

    def resolution_phase(self):
        # Determine order
        first = self.player
        second = self.opponent
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills
        for attacker in [first, second]:
            defender = self.opponent if attacker == self.player else self.player
            attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            
            skill = self.queued_skills[attacker.uid]
            damage = self.calculate_damage(skill, attacker_creature, defender_creature)
            
            defender_creature.hp = max(0, defender_creature.hp - damage)
            self._show_text(self.player, 
                f"{attacker_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")
            
            if defender_creature.hp == 0:
                break

        self.queued_skills.clear()

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
