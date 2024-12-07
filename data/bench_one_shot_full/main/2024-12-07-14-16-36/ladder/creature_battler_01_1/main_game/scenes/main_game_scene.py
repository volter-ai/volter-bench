from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        
        while True:
            # Player turn
            player_skill = self._handle_player_turn(self.player)
            bot_skill = self._handle_player_turn(self.bot)

            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)

            # Check win condition
            if self._check_battle_end():
                break

        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player):
        choices = [
            DictionaryChoice(skill.display_name) for skill in 
            (self.player_creature.skills if current_player == self.player else self.bot_creature.skills)
        ]
        choice = self._wait_for_choice(current_player, choices)
        return choice

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply player damage to bot creature
        self.bot_creature.hp -= self.player_creature.skills[0].damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        
        # Apply bot damage to player creature
        self.player_creature.hp -= self.bot_creature.skills[0].damage
        self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False
