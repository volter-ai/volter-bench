from mini_game_engine.engine.lib import AbstractGameScene, Button

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
        self._show_text(self.player, "A wild trainer appears!")
        
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
            self._show_text(self.player, f"You used {player_skill.display_name}!")
            self.bot_creature.hp -= self.player_creature.skills[0].damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.player_creature.hp = self.player_creature.max_hp  # Reset HP
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe used {bot_skill.display_name}!")
            self.player_creature.hp -= self.bot_creature.skills[0].damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.player_creature.hp = self.player_creature.max_hp  # Reset HP
                self._transition_to_scene("MainMenuScene")
                return
