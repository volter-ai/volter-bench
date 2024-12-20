from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in skills])

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _execute_turn(self, first, second, first_skill, second_skill):
        # Execute first attack
        damage = self._calculate_damage(first, second, first_skill)
        second.hp = max(0, second.hp - damage)
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name}!")
        self._show_text(self.player, f"It dealt {damage} damage!")

        if second.hp > 0:
            # Execute second attack
            damage = self._calculate_damage(second, first, second_skill)
            first.hp = max(0, first.hp - damage)
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")

    def run(self):
        while True:
            # Player choice
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice
            bot_skill_choices = [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            bot_skill = self.bot_creature.skills[bot_skill_choices.index(bot_choice)]

            # Determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first, second = self.player_creature, self.bot_creature
                first_skill, second_skill = player_skill, bot_skill
            elif self.player_creature.speed < self.bot_creature.speed:
                first, second = self.bot_creature, self.player_creature
                first_skill, second_skill = bot_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.bot_creature
                    first_skill, second_skill = player_skill, bot_skill
                else:
                    first, second = self.bot_creature, self.player_creature
                    first_skill, second_skill = bot_skill, player_skill

            self._execute_turn(first, second, first_skill, second_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
