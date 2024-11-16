import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, create_from_game_database
from main_game.models import Skill

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
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Attack: {self.bot_creature.attack}
Defense: {self.bot_creature.defense}
Speed: {self.bot_creature.speed}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot choice phase
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first[0], first[1], first[2], first[3])
            if self.check_battle_end():
                break
                
            self.execute_move(second[0], second[1], second[2], second[3])
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, self.bot_creature, self.player_choice), \
                   (self.bot, self.bot_creature, self.player_creature, self.bot_choice)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_creature, self.player_creature, self.bot_choice), \
                   (self.player, self.player_creature, self.bot_creature, self.player_choice)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.bot_creature, self.player_choice), \
                       (self.bot, self.bot_creature, self.player_creature, self.bot_choice)
            else:
                return (self.bot, self.bot_creature, self.player_creature, self.bot_choice), \
                       (self.player, self.player_creature, self.bot_creature, self.player_choice)

    def execute_move(self, attacker, attacker_creature, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.bot_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
