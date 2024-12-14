from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player, Creature, Skill
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            bot_skill = self.get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute skills in order
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.bot
                    defender_creature = self.bot_creature
                else:
                    defender = self.player
                    defender_creature = self.player_creature
                    
                damage = self.calculate_damage(skill, attacker_creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage to {defender_creature.display_name}!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    if defender == self.player:
                        self._show_text(self.player, "You lost!")
                    else:
                        self._show_text(self.player, "You won!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def get_skill_choice(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def determine_order(self, first_pair, second_pair):
        first_player, first_creature, first_skill = first_pair
        second_player, second_creature, second_skill = second_pair
        
        if first_creature.speed > second_creature.speed:
            return first_pair, second_pair
        elif second_creature.speed > first_creature.speed:
            return second_pair, first_pair
        else:
            if random.random() < 0.5:
                return first_pair, second_pair
            return second_pair, first_pair

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        return max(0, final_damage)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
