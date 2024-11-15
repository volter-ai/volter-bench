from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
        # Determine order
        player_first = True
        if self.opponent_creature.speed > self.player_creature.speed:
            player_first = False
        elif self.opponent_creature.speed == self.player_creature.speed:
            player_first = random.choice([True, False])
            
        if player_first:
            # Player attacks first
            damage = self.calculate_damage(self.player_creature, self.opponent_creature, player_skill)
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name} for {damage} damage!")
            
            if self.opponent_creature.hp > 0:
                # Opponent attacks second
                damage = self.calculate_damage(self.opponent_creature, self.player_creature, opponent_skill)
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name} for {damage} damage!")
        else:
            # Opponent attacks first
            damage = self.calculate_damage(self.opponent_creature, self.player_creature, opponent_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name} for {damage} damage!")
            
            if self.player_creature.hp > 0:
                # Player attacks second
                damage = self.calculate_damage(self.player_creature, self.opponent_creature, player_skill)
                self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = self.player_creature.skills[skill_choices.index(player_choice)]
            
            # Opponent choice phase
            opponent_skill_choices = [DictionaryChoice(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            opponent_skill = self.opponent_creature.skills[opponent_skill_choices.index(opponent_choice)]
            
            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
        
        self._transition_to_scene("MainMenuScene")
