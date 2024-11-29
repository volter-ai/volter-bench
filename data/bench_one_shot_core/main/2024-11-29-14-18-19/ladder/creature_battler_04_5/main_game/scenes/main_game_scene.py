from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures to max HP
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature)}"""

    def _format_skills(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def _calculate_damage(self, attacker_creature: Creature, defender_creature: Creature, skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _execute_turn(self, first_creature: Creature, second_creature: Creature, first_skill, second_skill):
        # First attack
        damage = self._calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Check if battle ended
        if second_creature.hp <= 0:
            return
            
        # Second attack
        damage = self._calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, self.player_creature.skills)
            
            # Bot choice phase
            bot_skill = self._wait_for_choice(self.bot, self.bot_creature.skills)
            
            # Resolution phase - determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first = (self.player_creature, self.bot_creature, player_skill, bot_skill)
            elif self.bot_creature.speed > self.player_creature.speed:
                first = (self.bot_creature, self.player_creature, bot_skill, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, self.bot_creature, player_skill, bot_skill)
                else:
                    first = (self.bot_creature, self.player_creature, bot_skill, player_skill)
                    
            self._execute_turn(*first)
            
            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
                
        self._transition_to_scene("MainMenuScene")
