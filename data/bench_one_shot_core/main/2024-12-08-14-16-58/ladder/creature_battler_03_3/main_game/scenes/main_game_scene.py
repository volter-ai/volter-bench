from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_chosen_skill = self.player_creature.skills[skill_buttons.index(choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[[skill.display_name for skill in self.bot_creature.skills].index(bot_choice.display_name)]

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(*first)
            if self.check_battle_end():
                return
                
            self.execute_move(*second)
            if self.check_battle_end():
                return

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player_creature, self.player_chosen_skill, self.bot_creature), (self.bot_creature, self.bot_chosen_skill, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot_creature, self.bot_chosen_skill, self.player_creature), (self.player_creature, self.player_chosen_skill, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_chosen_skill, self.bot_creature), (self.bot_creature, self.bot_chosen_skill, self.player_creature)
            return (self.bot_creature, self.bot_chosen_skill, self.player_creature), (self.player_creature, self.player_chosen_skill, self.bot_creature)

    def execute_move(self, attacker, skill, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

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
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
