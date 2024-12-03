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

VS

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
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = self.player_creature.skills[choices.index(player_choice)]

            # Bot Choice Phase
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[0]  # Bot only has tackle

            # Resolution Phase
            first, second = self.determine_turn_order()
            
            # Execute moves
            if not self.execute_move(first):
                return
            if not self.execute_move(second):
                return

    def determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)

    def execute_move(self, move_tuple):
        attacker, skill = move_tuple
        if attacker == self.player:
            damage = self.player_creature.attack + skill.base_damage - self.bot_creature.defense
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name} for {damage} damage!")
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return False
        else:
            damage = self.bot_creature.attack + skill.base_damage - self.player_creature.defense
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {skill.display_name} for {damage} damage!")
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return False
        return True
