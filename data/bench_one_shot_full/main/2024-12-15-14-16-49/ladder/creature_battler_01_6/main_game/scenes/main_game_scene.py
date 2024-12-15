from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player turn
            self._show_text(self.player, "Your turn!")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot turn
            self._show_text(self.bot, "Bot's turn!")
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution
            self._resolve_turn(player_skill, bot_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self, player_skill: Skill, bot_skill: Skill):
        # Apply player skill
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}!")

        # Apply bot skill if still alive
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player,
                f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
