from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player choice phase
            player_creature = self.player.creatures[0]
            skill_choices = [Button(skill.display_name) for skill in player_creature.skills]
            self.player_skill_choice = self._wait_for_choice(self.player, skill_choices)

            # Bot choice phase
            bot_creature = self.bot.creatures[0]
            bot_skill_choices = [Button(skill.display_name) for skill in bot_creature.skills]
            self.bot_skill_choice = self._wait_for_choice(self.bot, bot_skill_choices)

            # Resolution phase
            player_skill = player_creature.skills[0]  # Since we only have tackle
            bot_skill = bot_creature.skills[0]

            # Apply damage
            bot_creature.hp -= player_skill.damage
            self._show_text(self.player, f"Your {player_creature.display_name} used {player_skill.display_name}!")
            
            if bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Foe's {bot_creature.display_name} used {bot_skill.display_name}!")
            
            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before transitioning
        player_creature.hp = player_creature.max_hp
        bot_creature.hp = bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
