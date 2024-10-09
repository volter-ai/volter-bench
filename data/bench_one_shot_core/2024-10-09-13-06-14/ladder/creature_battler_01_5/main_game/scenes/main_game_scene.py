from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your Skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.description}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        while True:
            if self._check_battle_end():
                break

            player_skill = self._player_choice_phase()
            bot_skill = self._bot_choice_phase()
            self._resolution_phase(player_skill, bot_skill)

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")  # Add this line to return to the main menu

    def _player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        return skill_choice.thing

    def _bot_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        skill_choice = self._wait_for_choice(self.bot, skill_choices)
        return skill_choice.thing

    def _resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.bot, f"Foe used {bot_skill.display_name}!")

        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"You dealt {player_skill.damage} damage!")
        self._show_text(self.player, f"Foe dealt {bot_skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
