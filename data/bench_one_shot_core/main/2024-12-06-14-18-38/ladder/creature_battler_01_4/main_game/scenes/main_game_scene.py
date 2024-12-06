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
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in player_creature.skills])}
"""

    def _reset_creatures(self, player: Player):
        """Reset creatures to starting state"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player turn
            player_creature = self.player.creatures[0]
            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures(self.player)
                self._reset_creatures(self.bot)
                self._transition_to_scene("MainMenuScene")
                return

            # Bot turn  
            bot_creature = self.bot.creatures[0]
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures(self.player)
                self._reset_creatures(self.bot)
                self._transition_to_scene("MainMenuScene")
                return

            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            bot_skill_choices = [Button(skill.display_name) for skill in bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            bot_skill = bot_creature.skills[bot_skill_choices.index(bot_choice)]

            # Resolution phase
            self._show_text(self.player, f"You used {player_skill.display_name}!")
            bot_creature.hp -= player_skill.damage

            self._show_text(self.player, f"Foe used {bot_skill.display_name}!")
            player_creature.hp -= bot_skill.damage
