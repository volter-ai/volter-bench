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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute skills
            for attacker, creature, skill in [first, second]:
                if self._execute_skill(attacker, creature, skill):
                    return # Battle ended
                    
    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        return self._wait_for_choice(player, choices).value["skill"]
        
    def _determine_order(self, a, b):
        if a[1].speed > b[1].speed:
            return a, b
        elif b[1].speed > a[1].speed:
            return b, a
        else:
            return random.choice([(a,b), (b,a)])
            
    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.bot
            defender_creature = self.bot_creature
        else:
            defender = self.player
            defender_creature = self.player_creature
            
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")
        
        # Check for battle end
        if defender_creature.hp <= 0:
            if defender == self.player:
                self._show_text(self.player, "You lost!")
            else:
                self._show_text(self.player, "You won!")
                
            # Reset creatures
            self.player_creature.hp = self.player_creature.max_hp
            self.bot_creature.hp = self.bot_creature.max_hp
            
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
        
    def _get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
