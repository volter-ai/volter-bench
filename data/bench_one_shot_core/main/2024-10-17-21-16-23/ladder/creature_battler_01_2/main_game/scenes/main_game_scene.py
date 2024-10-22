from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, RandomModeGracefulExit
import time


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
        try:
            self._show_text(self.player, "A wild creature appears!")
            self._show_text(self.bot, "A wild creature appears!")

            while True:
                # Player turn
                player_skill = self._player_turn()
                
                # Bot turn
                bot_skill = self._bot_turn()
                
                # Resolution phase
                self._resolve_turn(player_skill, bot_skill)
                
                if self._check_battle_end():
                    break

            # Short delay to show the battle result
            time.sleep(1)

            # Reset creatures' state before transitioning
            self._reset_creatures()

            # Transition back to the main menu
            self._transition_to_scene("MainMenuScene")

        except RandomModeGracefulExit:
            # Handle the random testing scenario
            print("Random mode graceful exit in MainGameScene")
            # Ensure creatures are reset even in random mode
            self._reset_creatures()

    def _player_turn(self):
        self._show_text(self.player, "It's your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _bot_turn(self):
        self._show_text(self.bot, "It's your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, bot_skill):
        self._apply_damage(self.player, self.player_creature, player_skill, self.bot_creature)
        self._apply_damage(self.bot, self.bot_creature, bot_skill, self.player_creature)

    def _apply_damage(self, attacker, attacker_creature, skill, target_creature):
        damage = skill.damage
        target_creature.hp = max(0, target_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{target_creature.display_name} took {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
