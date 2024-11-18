from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.bot, "Battle start!")

        while True:
            # Player turn
            player_skill = self._handle_player_turn(self.player, self.player_creature)
            bot_skill = self._handle_player_turn(self.bot, self.bot_creature)

            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)

            if self._check_battle_end():
                break

    def _handle_player_turn(self, current_player, creature):
        choices = [
            DictionaryChoice(skill.display_name) for skill in creature.skills
        ]
        choice = self._wait_for_choice(current_player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.player, f"Foe used {bot_skill.display_name}!")

    def _reset_creatures(self):
        # Reset both player and bot creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
