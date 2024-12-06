from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

TYPE_EFFECTIVENESS = {
    "fire": {"water": 0.5, "leaf": 2.0},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        return int(raw_damage * effectiveness)

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp = max(0, second.hp - damage)
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second.hp > 0:
            # Second attack
            damage = self.calculate_damage(second, first, second_skill)
            first.hp = max(0, first.hp - damage)
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice
            player_skill = self._wait_for_choice(self.player, self.player_creature.skills)
            
            # Bot choice
            opponent_skill = self._wait_for_choice(self.opponent, self.opponent_creature.skills)

            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player_creature, self.opponent_creature
                first_skill, second_skill = player_skill, opponent_skill
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent_creature, self.player_creature
                first_skill, second_skill = opponent_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.opponent_creature
                    first_skill, second_skill = player_skill, opponent_skill
                else:
                    first, second = self.opponent_creature, self.player_creature
                    first_skill, second_skill = opponent_skill, player_skill

            self.execute_turn(first, second, first_skill, second_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")
