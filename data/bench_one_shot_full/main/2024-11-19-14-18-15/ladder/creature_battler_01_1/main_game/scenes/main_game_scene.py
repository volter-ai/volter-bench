from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        
        while True:
            # Player phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_skill = self.player_creature.skills[skill_buttons.index(choice)]

            # Bot phase
            bot_choice = self._wait_for_choice(self.bot, skill_buttons)
            self.bot_skill = self.bot_creature.skills[skill_buttons.index(bot_choice)]

            # Resolution phase
            self.bot_creature.hp -= self.player_skill.damage
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            self.player_creature.hp -= self.bot_skill.damage
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before exiting by setting hp back to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
