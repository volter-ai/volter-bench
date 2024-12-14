from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

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

    def execute_turn(self):
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
        second = self.opponent_creature if first == self.player_creature else self.player_creature
        
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills
        for attacker in [first, second]:
            defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
            skill = self.queued_skills[attacker.prototype_id]
            
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")

    def run(self):
        while True:
            # Player turn
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            selected_skill = next(s for s in self.player_creature.skills if s.display_name == choice.display_name)
            self.queued_skills[self.player_creature.prototype_id] = selected_skill

            # Bot turn
            bot_skill = self._wait_for_choice(self.opponent, self.opponent_creature.skills)
            self.queued_skills[self.opponent_creature.prototype_id] = bot_skill

            # Execute turn
            self.execute_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")
