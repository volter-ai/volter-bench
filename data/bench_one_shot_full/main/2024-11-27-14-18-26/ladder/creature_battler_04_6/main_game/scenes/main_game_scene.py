from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in skills])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def execute_turn(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {damage} damage!")

    def run(self):
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, self.player_creature.skills)
            bot_skill = self._wait_for_choice(self.bot, self.bot_creature.skills)

            # Determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first, second = (self.player_creature, self.bot_creature), (self.bot_creature, self.player_creature)
                first_skill, second_skill = player_skill, bot_skill
            elif self.player_creature.speed < self.bot_creature.speed:
                first, second = (self.bot_creature, self.player_creature), (self.player_creature, self.bot_creature)
                first_skill, second_skill = bot_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = (self.player_creature, self.bot_creature), (self.bot_creature, self.player_creature)
                    first_skill, second_skill = player_skill, bot_skill
                else:
                    first, second = (self.bot_creature, self.player_creature), (self.player_creature, self.bot_creature)
                    first_skill, second_skill = bot_skill, player_skill

            # Execute turns
            self.execute_turn(first[0], first[1], first_skill)
            if first[1].hp > 0:
                self.execute_turn(second[0], second[1], second_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
