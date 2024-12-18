from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures at start by setting hp to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.bot.display_name}!")
        
        while True:
            # Player turn
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot turn
            bot_skill = self._handle_turn(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, f"You won! {self.bot_creature.display_name} fainted!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, f"You lost! {self.player_creature.display_name} fainted!")
                break
        
        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player: Player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        
        # Find selected skill
        for skill in creature.skills:
            if skill.display_name == choice.display_name:
                return skill
                
    def _resolve_turn(self, player_skill, bot_skill):
        # Apply player skill
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}! "
            f"Dealt {player_skill.damage} damage!")
        
        # Apply bot skill if still alive
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player,
                f"Foe {self.bot_creature.display_name} used {bot_skill.display_name}! "
                f"Dealt {bot_skill.damage} damage!")
