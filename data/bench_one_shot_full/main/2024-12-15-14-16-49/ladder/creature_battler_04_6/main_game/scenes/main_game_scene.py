from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Enemy {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player phase
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_skill.display_name)

            # Bot phase  
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )
            bot_skill = next(s for s in self.bot_creature.skills 
                           if s.display_name == bot_skill.display_name)

            # Resolution phase
            first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
            second = self.bot_creature if first == self.player_creature else self.player_creature
            first_skill = player_skill if first == self.player_creature else bot_skill
            second_skill = bot_skill if first == self.player_creature else player_skill

            # Execute skills
            damage = self._calculate_damage(first, second, first_skill)
            if first == self.player_creature:
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"Your {first.display_name} dealt {damage} damage!")
            else:
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Enemy {first.display_name} dealt {damage} damage!")

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

            damage = self._calculate_damage(second, first, second_skill)
            if second == self.player_creature:
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"Your {second.display_name} dealt {damage} damage!")
            else:
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Enemy {second.display_name} dealt {damage} damage!")

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

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)
