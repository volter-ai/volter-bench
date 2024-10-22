from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        while True:
            # Player turn
            self._show_text(self.player, f"It's {self.player.display_name}'s turn!")
            player_skill = self._player_choose_skill(self.player)
            
            # Bot turn
            self._show_text(self.bot, f"It's {self.bot.display_name}'s turn!")
            bot_skill = self._player_choose_skill(self.bot)
            
            # Resolve turns
            self._resolve_turn(self.player, self.player_creature, player_skill, self.bot_creature)
            if self._check_battle_end():
                break
            
            self._resolve_turn(self.bot, self.bot_creature, bot_skill, self.player_creature)
            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choose_skill(self, current_player: Player) -> Skill:
        choices = [SelectThing(skill) for skill in current_player.creatures[0].skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolve_turn(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = skill.damage
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} fainted! You win!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
