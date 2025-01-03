import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player

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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot choice phase
            self.bot_chosen_skill = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute skills
            self.execute_skill(first[0], first[1], first[2], first[3])
            if self.check_battle_end():
                break
                
            self.execute_skill(second[0], second[1], second[2], second[3])
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, self.bot_creature, self.player_chosen_skill), \
                   (self.bot, self.bot_creature, self.player_creature, self.bot_chosen_skill)
        elif self.player_creature.speed < self.bot_creature.speed:
            return (self.bot, self.bot_creature, self.player_creature, self.bot_chosen_skill), \
                   (self.player, self.player_creature, self.bot_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.bot_creature, self.player_chosen_skill), \
                       (self.bot, self.bot_creature, self.player_creature, self.bot_chosen_skill)
            else:
                return (self.bot, self.bot_creature, self.player_creature, self.bot_chosen_skill), \
                       (self.player, self.player_creature, self.bot_creature, self.player_chosen_skill)

    def execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
