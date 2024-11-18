from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            self.player_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot choice phase
            self._show_text(self.bot, "Bot choosing skill...")
            self.bot_skill = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if self.check_battle_end():
                break
            self.execute_turn(second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_skill), (self.bot, self.bot_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_skill), (self.player, self.player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_skill), (self.bot, self.bot_skill)
            return (self.bot, self.bot_skill), (self.player, self.player_skill)

    def calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        factor = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                factor = 2.0
            elif defender.creature_type == "water":
                factor = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                factor = 2.0
            elif defender.creature_type == "leaf":
                factor = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                factor = 2.0
            elif defender.creature_type == "fire":
                factor = 0.5

        return int(raw_damage * factor)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.bot_creature
        else:
            attacker_creature = self.bot_creature
            defender_creature = self.player_creature

        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
