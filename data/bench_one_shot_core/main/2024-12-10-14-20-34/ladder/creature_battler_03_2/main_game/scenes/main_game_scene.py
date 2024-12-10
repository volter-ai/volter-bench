from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player_creature, player_skill, self.opponent_creature)
            second = (self.opponent_creature, opponent_skill, self.player_creature)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent_creature, opponent_skill, self.player_creature)
            second = (self.player_creature, player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                first = (self.player_creature, player_skill, self.opponent_creature)
                second = (self.opponent_creature, opponent_skill, self.player_creature)
            else:
                first = (self.opponent_creature, opponent_skill, self.player_creature)
                second = (self.player_creature, player_skill, self.opponent_creature)

        # Execute attacks
        for attacker, skill, defender in [first, second]:
            if defender.hp <= 0:
                continue
                
            damage = self.calculate_damage(skill, attacker, defender)
            defender.hp -= damage
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player turn
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            player_skill = player_choice.thing

            # Opponent turn
            opponent_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            opponent_skill = opponent_choice.thing

            # Execute turn
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
