from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
ATK: {self.player_creature.attack} DEF: {self.player_creature.defense} SPD: {self.player_creature.speed}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
ATK: {self.bot_creature.attack} DEF: {self.bot_creature.defense} SPD: {self.bot_creature.speed}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(
                self.player,
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Bot choice phase
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first)
            if self.check_battle_end():
                break
                
            self.execute_move(second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_move(self, attacker):
        if attacker == self.player:
            skill = self.player_creature.skills[0]  # Using tackle
            damage = self.player_creature.attack + skill.base_damage - self.bot_creature.defense
            self.bot_creature.hp -= max(1, damage)
            self._show_text(self.player, f"{self.player_creature.display_name} used {skill.display_name}!")
        else:
            skill = self.bot_creature.skills[0]  # Using tackle
            damage = self.bot_creature.attack + skill.base_damage - self.player_creature.defense
            self.player_creature.hp -= max(1, damage)
            self._show_text(self.bot, f"{self.bot_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._quit_whole_game()
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._quit_whole_game()
            return True
        return False
