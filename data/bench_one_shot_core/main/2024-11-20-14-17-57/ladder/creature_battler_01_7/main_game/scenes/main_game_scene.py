from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        self._show_text(self.bot, "A battle begins!")

        while True:
            # Player turn
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_choice.display_name)
            
            # Bot turn
            bot_choice = self._wait_for_choice(self.bot, skill_choices)
            bot_skill = next(s for s in self.bot_creature.skills 
                           if s.display_name == bot_choice.display_name)

            # Resolution
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self._show_text(self.bot, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
            
            self.bot_creature.hp -= player_skill.damage
            self.player_creature.hp -= bot_skill.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break

        # Reset creatures before exiting
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
