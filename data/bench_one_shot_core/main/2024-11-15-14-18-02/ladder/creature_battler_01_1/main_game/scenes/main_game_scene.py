from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self._show_text(self.bot, f"Battle starts against {self.player_creature.display_name}!")

        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot turn
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution phase
            self._show_text(self.player, f"You used {player_skill.display_name}!")
            self._show_text(self.bot, f"Foe used {bot_skill.display_name}!")
            
            self.bot_creature.hp -= player_skill.damage
            self.player_creature.hp -= bot_skill.damage

            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
