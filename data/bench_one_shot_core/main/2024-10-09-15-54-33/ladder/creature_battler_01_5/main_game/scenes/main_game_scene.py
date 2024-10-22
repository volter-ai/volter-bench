from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill_queue: List[Skill] = []
        self.bot_skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.damage} damage" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player turn
            player_skill = self.player_turn()
            if player_skill is None:
                return

            # Bot turn
            bot_skill = self.bot_turn()

            # Add skills to queues
            self.player_skill_queue.append(player_skill)
            self.bot_skill_queue.append(bot_skill)

            # Resolution phase
            self.resolve_turn()

            if self.check_battle_end():
                self.reset_creature_states()
                return

    def player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()
            return None

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        return skill_choice.thing

    def bot_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        skill_choice = self._wait_for_choice(self.bot, skill_choices)
        return skill_choice.thing

    def resolve_turn(self):
        while self.player_skill_queue or self.bot_skill_queue:
            if self.player_skill_queue:
                player_skill = self.player_skill_queue.pop(0)
                self._show_text(self.player, f"You used {player_skill.display_name}!")
                self.bot_creature.hp -= player_skill.damage
                self._show_text(self.player, f"The opponent's {self.bot_creature.display_name} took {player_skill.damage} damage!")

            if self.bot_skill_queue:
                bot_skill = self.bot_skill_queue.pop(0)
                self._show_text(self.player, f"The opponent's {self.bot_creature.display_name} used {bot_skill.display_name}!")
                self.player_creature.hp -= bot_skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} took {bot_skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.bot_creature.display_name} fainted! You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creature_states(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
