from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
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
            
        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp = max(0, second_creature.hp - damage)
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second_creature.hp <= 0:
            return
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp = max(0, first_creature.hp - damage)
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def reset_creatures(self):
        # Reset all creatures back to their max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def run(self):
        while True:
            # Player choice phase
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [DictionaryChoice(s.display_name) for s in self.opponent_creature.skills])
            opponent_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed:
                self.execute_turn(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                self.execute_turn(self.opponent_creature, self.player_creature, opponent_skill, player_skill)
            else:
                if random.random() < 0.5:
                    self.execute_turn(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
                else:
                    self.execute_turn(self.opponent_creature, self.player_creature, opponent_skill, player_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.reset_creatures()  # Reset creatures before transitioning
                self._transition_to_scene("MainMenuScene")
                return
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.reset_creatures()  # Reset creatures before transitioning
                self._transition_to_scene("MainMenuScene") 
                return
