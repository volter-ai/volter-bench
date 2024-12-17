from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

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
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def _reset_creatures(self):
        # Reset all creatures to their max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def _end_battle(self, message_to_player: str, message_to_bot: str):
        self._show_text(self.player, message_to_player)
        self._show_text(self.bot, message_to_bot)
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.queued_skills.append((self.player, player_choice.thing))

            # Bot phase
            bot_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.queued_skills.append((self.bot, bot_choice.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    self.bot_creature.hp -= skill.damage
                    self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Foe's {self.player_creature.display_name} used {skill.display_name}!")
                    if self.bot_creature.hp <= 0:
                        self._end_battle("You won!", "You lost!")
                        return
                else:
                    self.player_creature.hp -= skill.damage
                    self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {skill.display_name}!")
                    if self.player_creature.hp <= 0:
                        self._end_battle("You lost!", "You won!")
                        return

            self.queued_skills.clear()
