from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_choice = self._wait_for_choice(self.player, choices).thing

            # Bot Choice Phase
            self.bot_choice = self._wait_for_choice(self.bot, 
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_skill(first[0], first[1], first[2], first[3])
            if self.check_battle_end():
                break
                
            self.execute_skill(second[0], second[1], second[2], second[3])
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_choice, self.bot, self.bot_creature), \
                   (self.bot, self.bot_choice, self.player, self.player_creature)
        elif self.player_creature.speed < self.bot_creature.speed:
            return (self.bot, self.bot_choice, self.player, self.player_creature), \
                   (self.player, self.player_choice, self.bot, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_choice, self.bot, self.bot_creature), \
                       (self.bot, self.bot_choice, self.player, self.player_creature)
            else:
                return (self.bot, self.bot_choice, self.player, self.player_creature), \
                       (self.player, self.player_choice, self.bot, self.bot_creature)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def execute_skill(self, attacker, skill, defender, defender_creature):
        # Convert all values to float for intermediate calculations
        attack = float(attacker.creatures[0].attack)
        base_damage = float(skill.base_damage)
        defense = float(defender_creature.defense)
        
        # Calculate raw damage using floats
        raw_damage = attack + base_damage - defense
        
        # Get type multiplier (already returns float)
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        # Calculate final damage using floats, then convert to int at the end
        final_damage = int(raw_damage * multiplier)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {skill.display_name} deals {final_damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
