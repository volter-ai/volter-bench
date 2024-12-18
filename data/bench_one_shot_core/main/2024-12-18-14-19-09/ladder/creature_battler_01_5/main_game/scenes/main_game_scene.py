from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature

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
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def reset_creatures(self):
        # Reset player creatures by recreating them from prototypes
        for i, creature in enumerate(self.player.creatures):
            fresh_creature = create_from_game_database(creature.prototype_id, Creature)
            self.player.creatures[i] = fresh_creature
            
        # Reset bot creatures
        for i, creature in enumerate(self.bot.creatures):
            fresh_creature = create_from_game_database(creature.prototype_id, Creature)
            self.bot.creatures[i] = fresh_creature

    def run(self):
        self._show_text(self.player, "A battle begins!")
        self._show_text(self.bot, "A battle begins!")

        while True:
            # Player phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.queued_skills.append((self.player, player_choice.thing))

            # Bot phase
            bot_choice = self._wait_for_choice(self.bot, choices)
            self.queued_skills.append((self.bot, bot_choice.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    self.bot_creature.hp -= skill.damage
                    self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Foe's {self.player_creature.display_name} used {skill.display_name}!")
                    if self.bot_creature.hp <= 0:
                        self._show_text(self.player, "You won!")
                        self._show_text(self.bot, "You lost!")
                        self.reset_creatures()  # Reset before transitioning
                        self._transition_to_scene("MainMenuScene")
                        return
                else:
                    self.player_creature.hp -= skill.damage
                    self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {skill.display_name}!")
                    self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {skill.display_name}!")
                    if self.player_creature.hp <= 0:
                        self._show_text(self.player, "You lost!")
                        self._show_text(self.bot, "You won!")
                        self.reset_creatures()  # Reset before transitioning
                        self._transition_to_scene("MainMenuScene") 
                        return

            self.queued_skills = []
