from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

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
{chr(10).join([f"> {skill.display_name} (DMG: {skill.damage})" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Bot choice phase
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            player_skill_obj = next(s for s in self.player_creature.skills if s.display_name == player_skill.display_name)
            bot_skill_obj = next(s for s in self.bot_creature.skills if s.display_name == bot_skill.display_name)

            # Apply damage
            self.bot_creature.hp -= player_skill_obj.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill_obj.display_name}!")
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self.player_creature.hp -= bot_skill_obj.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill_obj.display_name}!")

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _reset_creatures(self):
        """Reset creature HP to max before leaving scene"""
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
