from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures by setting hp to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A {self.bot_creature.display_name} appears!")
        
        while True:
            # Player choice phase
            player_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            bot_skill = self.get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute skills
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.bot
                    defender_creature = self.bot_creature
                else:
                    defender = self.player
                    defender_creature = self.player_creature
                    
                damage = self.calculate_damage(skill, attacker_creature, defender_creature)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                
                self._show_text(self.player, 
                    f"{attacker_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")
                
                if defender_creature.hp <= 0:
                    if defender == self.bot:
                        self._show_text(self.player, "You won!")
                    else:
                        self._show_text(self.player, "You lost!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        return self._wait_for_choice(player, choices).value["skill"]

    def determine_order(self, first_pair, second_pair):
        if first_pair[1].speed > second_pair[1].speed:
            return first_pair, second_pair
        elif first_pair[1].speed < second_pair[1].speed:
            return second_pair, first_pair
        else:
            import random
            return random.choice([(first_pair, second_pair), (second_pair, first_pair)])

    def calculate_damage(self, skill: Skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
