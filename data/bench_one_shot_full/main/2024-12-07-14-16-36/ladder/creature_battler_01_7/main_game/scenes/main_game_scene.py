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

            # Check win conditions
            if self._check_battle_end():
                break

    def _handle_player_turn(self, current_player):
        creature = self.player_creature if current_player == self.player else self.bot_creature
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _check_battle_end(self):
        if self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene") 
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
