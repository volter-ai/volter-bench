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
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player choice phase
            player_creature = self.player.creatures[0]
            choices = [Button(skill.display_name) for skill in player_creature.skills]
            self.player_skill_choice = self._wait_for_choice(self.player, choices)

            # Bot choice phase  
            bot_creature = self.bot.creatures[0]
            bot_choices = [Button(skill.display_name) for skill in bot_creature.skills]
            self.bot_skill_choice = self._wait_for_choice(self.bot, bot_choices)

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self.bot.creatures[0].hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before leaving
        self.player.creatures[0].hp = self.player.creatures[0].max_hp
        self.bot.creatures[0].hp = self.bot.creatures[0].max_hp
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        # Apply player skill
        player_skill = next(s for s in self.player.creatures[0].skills 
                          if s.display_name == self.player_skill_choice.display_name)
        self.bot.creatures[0].hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player.creatures[0].display_name} used {player_skill.display_name}!")

        # Apply bot skill if still alive
        if self.bot.creatures[0].hp > 0:
            bot_skill = next(s for s in self.bot.creatures[0].skills 
                           if s.display_name == self.bot_skill_choice.display_name)
            self.player.creatures[0].hp -= bot_skill.damage
            self._show_text(self.player, f"Foe's {self.bot.creatures[0].display_name} used {bot_skill.display_name}!")
