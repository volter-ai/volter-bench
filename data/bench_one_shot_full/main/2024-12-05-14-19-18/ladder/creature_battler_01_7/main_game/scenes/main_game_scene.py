from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_actions = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_choice.display_name)
            
            # Bot phase
            bot_skill = self._wait_for_choice(self.bot, 
                [Button(skill.display_name) for skill in self.bot_creature.skills]).display_name
            bot_skill = next(s for s in self.bot_creature.skills if s.display_name == bot_skill)

            # Resolution phase
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self.bot_creature.hp -= player_skill.damage
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
                
            self._show_text(self.player, f"Foe {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self.player_creature.hp -= bot_skill.damage
            
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
