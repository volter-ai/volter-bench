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
            bot_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            self.bot_choice = self._wait_for_choice(self.bot, bot_choices).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first[0], first[1], first[2], first[3])
            if self.check_battle_end():
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return
                
            self.execute_move(second[0], second[1], second[2], second[3])
            if self.check_battle_end():
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, self.player_choice, self.bot_creature), \
                   (self.bot, self.bot_creature, self.bot_choice, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_creature, self.bot_choice, self.player_creature), \
                   (self.player, self.player_creature, self.player_choice, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_choice, self.bot_creature), \
                       (self.bot, self.bot_creature, self.bot_choice, self.player_creature)
            else:
                return (self.bot, self.bot_creature, self.bot_choice, self.player_creature), \
                       (self.player, self.player_creature, self.player_choice, self.bot_creature)

    def execute_move(self, attacker, attacker_creature, skill, defender_creature):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False
