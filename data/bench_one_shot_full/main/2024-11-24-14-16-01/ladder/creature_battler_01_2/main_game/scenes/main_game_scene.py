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
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player turn
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot turn
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self._show_text(self.bot, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
            
            self.bot_creature.hp -= player_skill.damage
            self.player_creature.hp -= bot_skill.damage

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

    def _get_skill_choice(self, player: Player, creature: Creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing
