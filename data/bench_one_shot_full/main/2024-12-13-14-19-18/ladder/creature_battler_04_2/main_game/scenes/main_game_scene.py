from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.reset_creatures()

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

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

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Check if battle ended
        if second.hp <= 0:
            return first
            
        # Second attack
        damage = self.calculate_damage(second, first, second_skill)
        first.hp -= damage
        self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")
        
        if first.hp <= 0:
            return second
            
        return None

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(
                self.player,
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_skill.display_name)

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )
            opponent_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_skill.display_name)

            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = self.player_creature
                second = self.opponent_creature
                first_skill = player_skill
                second_skill = opponent_skill
            elif self.opponent_creature.speed > self.player_creature.speed:
                first = self.opponent_creature
                second = self.player_creature
                first_skill = opponent_skill
                second_skill = player_skill
            else:
                if random.random() < 0.5:
                    first = self.player_creature
                    second = self.opponent_creature
                    first_skill = player_skill
                    second_skill = opponent_skill
                else:
                    first = self.opponent_creature
                    second = self.player_creature
                    first_skill = opponent_skill
                    second_skill = player_skill

            # Execute turn
            winner = self.execute_turn(first, second, first_skill, second_skill)
            
            if winner:
                if winner == self.player_creature:
                    self._show_text(self.player, "You won!")
                else:
                    self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
