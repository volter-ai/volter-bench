from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        self._show_text(self.bot, "A battle begins!")

        while True:
            # Player Choice Phase
            self.player_queued_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_queued_skill = self._handle_player_turn(self.bot, self.bot_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player: Player, current_creature: Creature):
        choices = [SelectThing(skill) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolve_turn(self):
        # Apply player's skill
        self.bot_creature.hp -= self.player_queued_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_queued_skill.display_name}!")
        self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {self.player_queued_skill.display_name}!")

        # Apply bot's skill
        self.player_creature.hp -= self.bot_queued_skill.damage
        self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.bot_queued_skill.display_name}!")
        self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_queued_skill.display_name}!")
