from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Player's turn:
{self._get_skill_choices_str(self.player_creature)}

Bot's turn:
{self._get_skill_choices_str(self.bot_creature)}
"""

    def _get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            bot_skill = self._player_choice_phase(self.bot, self.bot_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, bot_skill)

            # Check for battle end
            if self._check_battle_end():
                break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.bot, f"{self.bot.display_name}'s {self.bot_creature.display_name} used {bot_skill.display_name}!")

        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} took {player_skill.damage} damage!")
        self._show_text(self.bot, f"{self.player.display_name}'s {self.player_creature.display_name} took {bot_skill.damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self._show_text(self.bot, f"You defeated {self.player.display_name}'s {self.player_creature.display_name}! You won the battle.")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"You defeated {self.bot.display_name}'s {self.bot_creature.display_name}! You won the battle.")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} fainted! You lost the battle.")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
