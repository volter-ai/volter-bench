from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_queued_skill = None
        self.bot_queued_skill = None

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_queued_skill = self.player_creature.skills[skill_buttons.index(choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, skill_buttons)
            self.bot_queued_skill = self.bot_creature.skills[skill_buttons.index(bot_choice)]

            # Resolution phase
            self.bot_creature.hp -= self.player_queued_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_queued_skill.display_name}!")
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self.player_creature.hp -= self.bot_queued_skill.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {self.bot_queued_skill.display_name}!")

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
