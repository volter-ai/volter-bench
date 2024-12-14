from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate base damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def execute_turn(self, player_skill, bot_skill):
        # Determine order
        player_first = True
        if self.bot_creature.speed > self.player_creature.speed:
            player_first = False
        elif self.bot_creature.speed == self.player_creature.speed:
            player_first = random.choice([True, False])

        if player_first:
            # Player attacks first
            damage = self.calculate_damage(self.player_creature, self.bot_creature, player_skill)
            self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}! Dealt {damage} damage!")
            
            if self.bot_creature.hp > 0:
                # Bot attacks second
                damage = self.calculate_damage(self.bot_creature, self.player_creature, bot_skill)
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}! Dealt {damage} damage!")
        else:
            # Bot attacks first
            damage = self.calculate_damage(self.bot_creature, self.player_creature, bot_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}! Dealt {damage} damage!")
            
            if self.player_creature.hp > 0:
                # Player attacks second
                damage = self.calculate_damage(self.player_creature, self.bot_creature, player_skill)
                self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}! Dealt {damage} damage!")

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")

        while True:
            # Player choice phase
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills])
            bot_skill = self.bot_creature.skills[0]  # Bot always uses first skill for simplicity

            # Resolution phase
            self.execute_turn(player_skill, bot_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                break
