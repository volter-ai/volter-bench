from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

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
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Bot choice phase  
            self._show_text(self.bot, "Choose your skill!")
            bot_skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            self.bot_skill = self._wait_for_choice(self.bot, bot_skill_choices).thing

            # Resolution phase
            self._resolve_turn()

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

    def _resolve_turn(self):
        # Player's skill
        self.bot_creature.hp -= self.player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_skill.display_name}!")
        self._show_text(self.bot, f"Foe's {self.player_creature.display_name} used {self.player_skill.display_name}!")

        # Bot's skill
        self.player_creature.hp -= self.bot_skill.damage
        self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {self.bot_skill.display_name}!")
        self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_skill.display_name}!")
