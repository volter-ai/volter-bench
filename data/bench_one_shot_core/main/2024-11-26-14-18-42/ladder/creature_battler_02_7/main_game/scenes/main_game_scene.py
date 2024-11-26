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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Attack: {self.bot_creature.attack}
Defense: {self.bot_creature.defense}
Speed: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Bot Choice Phase
            self.bot_chosen_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute first attack
            damage = self.calculate_damage(first)
            if first == self.player:
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} dealt {damage} damage!")
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()  # Changed from return to _quit_whole_game()
            else:
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Enemy {self.bot_creature.display_name} dealt {damage} damage!")
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()  # Changed from return to _quit_whole_game()

            # Execute second attack
            damage = self.calculate_damage(second)
            if second == self.player:
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} dealt {damage} damage!")
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()  # Changed from return to _quit_whole_game()
            else:
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Enemy {self.bot_creature.display_name} dealt {damage} damage!")
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()  # Changed from return to _quit_whole_game()

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def calculate_damage(self, attacker):
        if attacker == self.player:
            return (self.player_creature.attack + 
                   self.player_creature.skills[0].base_damage - 
                   self.bot_creature.defense)
        else:
            return (self.bot_creature.attack + 
                   self.bot_creature.skills[0].base_damage - 
                   self.player_creature.defense)
