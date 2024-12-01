from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def _reset_creature(self, creature: Creature):
        creature.hp = creature.max_hp

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_choice = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot Choice Phase
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution Phase
            self._resolve_turn()

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break

        # Reset creatures before leaving
        self._reset_creature(self.player_creature)
        self._reset_creature(self.bot_creature)
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        # Player's skill
        self.bot_creature.hp -= self.player_choice.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_choice.display_name}!")
        self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {self.player_choice.display_name}!")

        # Bot's skill
        self.player_creature.hp -= self.bot_choice.damage
        self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.bot_choice.display_name}!")
        self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_choice.display_name}!")
