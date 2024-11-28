from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{chr(10).join([f"> {skill.display_name} (DMG: {skill.damage})" for skill in player_creature.skills])}
"""

    def _reset_creatures(self, player: Player):
        """Reset creatures to max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player choice phase
            player_creature = self.player.creatures[0]
            choices = [DictionaryChoice(skill.display_name) for skill in player_creature.skills]
            self.player_skill_choice = player_creature.skills[
                choices.index(self._wait_for_choice(self.player, choices))
            ]

            # Bot choice phase
            bot_creature = self.bot.creatures[0]
            bot_choices = [DictionaryChoice(skill.display_name) for skill in bot_creature.skills]
            self.bot_skill_choice = bot_creature.skills[
                bot_choices.index(self._wait_for_choice(self.bot, bot_choices))
            ]

            # Resolution phase
            self._show_text(self.player, f"You used {self.player_skill_choice.display_name}!")
            bot_creature.hp -= self.player_skill_choice.damage
            
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures(self.player)
                self._reset_creatures(self.bot)
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe used {self.bot_skill_choice.display_name}!")
            player_creature.hp -= self.bot_skill_choice.damage

            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures(self.player)
                self._reset_creatures(self.bot)
                self._transition_to_scene("MainMenuScene")
                return
