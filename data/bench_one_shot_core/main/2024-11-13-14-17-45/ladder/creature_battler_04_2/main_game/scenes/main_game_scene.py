from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Opponent choice phase
            self.opponent_choice = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                if self.check_battle_end():
                    break
            else:
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            if attacker == self.player:
                raw_damage = self.player_creature.attack + skill.base_damage - self.opponent_creature.defense
            else:
                raw_damage = self.opponent_creature.attack + skill.base_damage - self.player_creature.defense
        else:
            if attacker == self.player:
                raw_damage = (self.player_creature.sp_attack / self.opponent_creature.sp_defense) * skill.base_damage
            else:
                raw_damage = (self.opponent_creature.sp_attack / self.player_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        if attacker == self.player:
            defender_type = self.opponent_creature.creature_type
        else:
            defender_type = self.player_creature.creature_type

        effectiveness = self.get_type_effectiveness(skill.skill_type, defender_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, attacker):
        if attacker == self.player:
            skill = next(s for s in self.player_creature.skills if s.display_name == self.player_choice.display_name)
            damage = self.calculate_damage(attacker, self.opponent, skill)
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
            self._show_text(self.player, f"{self.player_creature.display_name} used {skill.display_name} for {damage} damage!")
        else:
            skill = next(s for s in self.opponent_creature.skills if s.display_name == self.opponent_choice.display_name)
            damage = self.calculate_damage(attacker, self.player, skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"{self.opponent_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} has been defeated!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} is victorious!")
            return True
        return False
