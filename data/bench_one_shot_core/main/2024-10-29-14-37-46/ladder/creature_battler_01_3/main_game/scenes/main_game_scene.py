from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


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

Your skills:
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

            self._player_turn()
            if self._check_battle_end():
                break

            self._bot_turn()

        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

        if choice == use_skill_button:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            self._use_skill(self.player_creature, self.bot_creature, skill_choice.thing)
        elif choice == quit_button:
            self._quit_whole_game()

    def _bot_turn(self):
        bot_skill = self.bot_creature.skills[0]  # Always use the first skill for simplicity
        self._use_skill(self.bot_creature, self.player_creature, bot_skill)

    def _use_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        defender.hp = max(0, defender.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
