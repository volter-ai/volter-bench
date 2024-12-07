from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
        self._show_text(self.player, "A wild creature appears!")
        
        while True:
            # Player turn
            player_skill = self._handle_player_turn()
            
            # Bot turn
            bot_skill = self._handle_bot_turn()
            
            # Resolution
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win conditions
            battle_result = self._check_battle_end()
            if battle_result is not None:
                # Reset creatures before transitioning
                self.player_creature.hp = self.player_creature.max_hp
                self.bot_creature.hp = self.bot_creature.max_hp
                
                if battle_result:
                    self._show_text(self.player, "Congratulations! You've won the game!")
                    self._quit_whole_game()
                else:
                    self._show_text(self.player, "Better luck next time!")
                    self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self):
        choices = [
            DictionaryChoice(skill.display_name) for skill in self.player_creature.skills
        ]
        self._show_text(self.player, "Choose your move!")
        choice = self._wait_for_choice(self.player, choices)
        return self.player_creature.skills[choices.index(choice)]

    def _handle_bot_turn(self):
        choices = [
            DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills
        ]
        self._show_text(self.bot, "Bot choosing move...")
        choice = self._wait_for_choice(self.bot, choices)
        return self.bot_creature.skills[choices.index(choice)]

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply player skill
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        
        # Apply bot skill
        self.player_creature.hp -= bot_skill.damage
        self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _check_battle_end(self):
        """Returns True for player victory, False for player defeat, None if battle continues"""
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return False
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return None
