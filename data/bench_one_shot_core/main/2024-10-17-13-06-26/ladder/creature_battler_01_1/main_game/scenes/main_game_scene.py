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

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.bot_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            bot_skill = self._player_choice_phase(self.bot, self.bot_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, bot_skill)
            
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self._apply_damage(self.bot_creature, player_skill)
        self._apply_damage(self.player_creature, bot_skill)

    def _apply_damage(self, target: Creature, skill: Skill):
        target.hp = max(0, target.hp - skill.damage)

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
