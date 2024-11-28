from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        # Reset creatures to full HP
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
            # Player turn
            player_creature = self.player.creatures[0]
            bot_creature = self.bot.creatures[0]

            # Player choice phase
            player_skill = self._get_skill_choice(self.player, player_creature)

            # Bot choice phase  
            bot_skill = self._get_skill_choice(self.bot, bot_creature)

            # Resolution phase
            self._show_text(self.player, f"Your {player_creature.display_name} used {player_skill.display_name}!")
            bot_creature.hp -= player_skill.damage
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe's {bot_creature.display_name} used {bot_skill.display_name}!")
            player_creature.hp -= bot_skill.damage
            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return

    def _get_skill_choice(self, player: Player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        return self._wait_for_choice(player, choices).value["skill"]
