from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{chr(10).join([f"> {skill.display_name} - {skill.damage} damage" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self._show_text(self.bot, f"Battle starts against {self.player_creature.display_name}!")

        while True:
            # Player turn
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)

            if self._check_battle_end():
                break

        self._reset_creatures()

    def _get_skill_choice(self, player: Player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.bot, f"Took {player_skill.damage} damage!")

        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.bot, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self._show_text(self.player, f"Took {bot_skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
