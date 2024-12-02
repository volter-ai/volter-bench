from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures at start
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player turn
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            player_skill_obj = next(s for s in self.player_creature.skills if s.display_name == player_skill.display_name)

            # Bot turn
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )
            bot_skill_obj = next(s for s in self.bot_creature.skills if s.display_name == bot_skill.display_name)

            # Resolution
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill_obj.display_name}!")
            self.bot_creature.hp -= player_skill_obj.damage
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            self._show_text(self.player, f"Foe {self.bot_creature.display_name} used {bot_skill_obj.display_name}!")
            self.player_creature.hp -= bot_skill_obj.damage
            
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset all player creatures before transitioning out
        for creature in self.player.creatures:
            creature.hp = creature.max_hp

        self._transition_to_scene("MainMenuScene")
