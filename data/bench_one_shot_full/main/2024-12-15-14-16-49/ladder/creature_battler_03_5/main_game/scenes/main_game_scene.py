from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
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

    def execute_turn(self, player_skill, bot_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            first = (self.player_creature, self.bot_creature, player_skill)
            second = (self.bot_creature, self.player_creature, bot_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            first = (self.bot_creature, self.player_creature, bot_skill)
            second = (self.player_creature, self.bot_creature, player_skill)
        else:
            if random.random() < 0.5:
                first = (self.player_creature, self.bot_creature, player_skill)
                second = (self.bot_creature, self.player_creature, bot_skill)
            else:
                first = (self.bot_creature, self.player_creature, bot_skill)
                second = (self.player_creature, self.bot_creature, player_skill)

        # Execute attacks in order
        for attacker, defender, skill in [first, second]:
            if defender.hp > 0:  # Only attack if defender is still alive
                damage = self.calculate_damage(attacker, defender, skill)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.bot.display_name}")

        while True:
            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Bot choice phase
            bot_skill = self.bot_creature.skills[random.randint(0, len(self.bot_creature.skills)-1)]

            # Resolution phase
            self.execute_turn(player_skill, bot_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, f"Victory! {self.player.display_name} wins!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, f"Defeat! {self.bot.display_name} wins!")
                break

        self._transition_to_scene("MainMenuScene")
