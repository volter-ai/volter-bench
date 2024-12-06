from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        # Reset creatures at start of battle
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
        
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player turn
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot turn
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_skills(player_skill, bot_skill)
            
            # Check win conditions
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player: Player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage
        
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}!\n"
            f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
