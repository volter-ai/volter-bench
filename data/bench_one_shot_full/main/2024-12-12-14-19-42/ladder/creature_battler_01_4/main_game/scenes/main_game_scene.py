from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        status = f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
"""
        for skill in self.player_creature.skills:
            status += f"> {skill.display_name} ({skill.damage} damage)\n"
        return status

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.bot, "Battle start!")

        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_choice = self.player_creature.skills[skill_buttons.index(player_choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, skill_buttons)
            self.bot_choice = self.bot_creature.skills[skill_buttons.index(bot_choice)]

            # Resolution phase
            self._show_text(self.player, f"You used {self.player_choice.display_name}!")
            self.bot_creature.hp -= self.player_choice.damage
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            self._show_text(self.player, f"Foe used {self.bot_choice.display_name}!")
            self.player_creature.hp -= self.bot_choice.damage
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
