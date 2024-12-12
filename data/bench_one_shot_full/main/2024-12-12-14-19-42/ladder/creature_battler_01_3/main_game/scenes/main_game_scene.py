from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_skill_choice = None
        self.bot_skill_choice = None
        
    def __str__(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.bot, "Battle start!")
        
        while True:
            # Player choice phase
            player_creature = self.player.creatures[0]
            choices = [Button(skill.display_name) for skill in player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.player_skill_choice = player_creature.skills[choices.index(choice)]

            # Bot choice phase
            bot_creature = self.bot.creatures[0]
            bot_choices = [Button(skill.display_name) for skill in bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.bot_skill_choice = bot_creature.skills[bot_choices.index(bot_choice)]

            # Resolution phase
            bot_creature.hp -= self.player_skill_choice.damage
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break

            player_creature.hp -= self.bot_skill_choice.damage
            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break

        # Reset creatures before exiting
        player_creature.hp = player_creature.max_hp
        bot_creature.hp = bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
