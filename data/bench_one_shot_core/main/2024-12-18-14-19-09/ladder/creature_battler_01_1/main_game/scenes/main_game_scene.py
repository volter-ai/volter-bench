from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill_choice = None
        self.bot_skill_choice = None

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        self._show_text(self.bot, "Battle start!")

        while True:
            # Player choice phase
            self.player_skill_choice = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot choice phase
            self.bot_skill_choice = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        # Player's skill
        self.bot_creature.hp -= self.player_skill_choice.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_skill_choice.display_name}!")
        self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {self.player_skill_choice.display_name}!")

        # Bot's skill
        if self.bot_creature.hp > 0:  # Only if bot creature still alive
            self.player_creature.hp -= self.bot_skill_choice.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {self.bot_skill_choice.display_name}!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_skill_choice.display_name}!")
