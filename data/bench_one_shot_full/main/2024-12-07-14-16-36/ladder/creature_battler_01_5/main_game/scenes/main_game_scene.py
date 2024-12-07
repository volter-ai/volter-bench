from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player turn
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Bot turn
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)

            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _resolve_turn(self, player_skill, bot_skill):
        # Get the actual skill objects
        p_skill = next(s for s in self.player_creature.skills if s.display_name == player_skill.display_name)
        b_skill = next(s for s in self.bot_creature.skills if s.display_name == bot_skill.display_name)

        # Apply damage
        self.bot_creature.hp -= p_skill.damage
        self.player_creature.hp -= b_skill.damage

        self._show_text(self.player, f"You used {p_skill.display_name}!")
        self._show_text(self.bot, f"Foe used {b_skill.display_name}!")

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
