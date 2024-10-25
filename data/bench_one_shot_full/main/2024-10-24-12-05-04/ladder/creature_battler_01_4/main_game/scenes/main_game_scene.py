from mini_game_engine.engine.lib import AbstractGameScene, Button
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

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            use_skill_button = Button("Use skill")
            quit_button = Button("Quit")
            choices = [use_skill_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if use_skill_button == choice:
                self._battle_turn()
                if self._check_battle_end():
                    self._reset_creatures()
                    self._transition_to_scene("MainMenuScene")
                    return
            elif quit_button == choice:
                self._transition_to_scene("MainMenuScene")
                return

    def _battle_turn(self):
        player_skill = self._choose_skill(self.player, self.player_creature)
        bot_skill = self._choose_skill(self.bot, self.bot_creature)

        self._resolve_skills(player_skill, bot_skill)

    def _choose_skill(self, player: Player, creature: Creature) -> Skill:
        skill_choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, skill_choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_skills(self, player_skill: Skill, bot_skill: Skill):
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.bot, f"Your {self.bot_creature.display_name} took {player_skill.damage} damage!")

        self.player_creature.hp -= bot_skill.damage
        self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {bot_skill.display_name}!")
        self._show_text(self.player, f"Your {self.player_creature.display_name} took {bot_skill.damage} damage!")

    def _check_battle_end(self) -> bool:
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
