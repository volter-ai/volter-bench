from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.queued_skills.append((self.player, player_choice.thing))

            # Bot phase
            bot_skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            self.queued_skills.append((self.bot, bot_choice.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    self.bot_creature.hp -= skill.damage
                    self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Foe's {self.player_creature.display_name} used {skill.display_name}!")
                else:
                    self.player_creature.hp -= skill.damage
                    self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {skill.display_name}!")

            self.queued_skills.clear()

            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
