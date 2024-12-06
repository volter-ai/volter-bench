from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_skill_choice = None
        self.bot_skill_choice = None
        
        # Reset creatures to full health
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            player_creature = self.player.creatures[0]
            choices = [SelectThing(skill) for skill in player_creature.skills]
            self.player_skill_choice = self._wait_for_choice(self.player, choices).thing

            # Bot choice phase
            bot_creature = self.bot.creatures[0]
            choices = [SelectThing(skill) for skill in bot_creature.skills]
            self.bot_skill_choice = self._wait_for_choice(self.bot, choices).thing

            # Resolution phase
            bot_creature.hp -= self.player_skill_choice.damage
            self._show_text(self.player, f"Your {player_creature.display_name} used {self.player_skill_choice.display_name}!")
            
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            player_creature.hp -= self.bot_skill_choice.damage
            self._show_text(self.player, f"Foe's {bot_creature.display_name} used {self.bot_skill_choice.display_name}!")

            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
