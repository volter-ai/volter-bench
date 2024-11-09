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
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            self.queued_skills.append((self.player, player_skill.thing))

            # Bot turn
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])
            self.queued_skills.append((self.bot, bot_skill.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    self.bot_creature.hp -= skill.damage
                    self._show_text(self.player, 
                        f"Your {self.player_creature.display_name} used {skill.display_name}!")
                    if self.bot_creature.hp <= 0:
                        self._show_text(self.player, "You won!")
                        self._reset_creatures()
                        self._transition_to_scene("MainMenuScene")
                        return
                else:
                    self.player_creature.hp -= skill.damage
                    self._show_text(self.player,
                        f"Foe's {self.bot_creature.display_name} used {skill.display_name}!")
                    if self.player_creature.hp <= 0:
                        self._show_text(self.player, "You lost!")
                        self._reset_creatures()
                        self._transition_to_scene("MainMenuScene")
                        return

            self.queued_skills.clear()

    def _reset_creatures(self):
        """Reset creatures to initial state"""
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
