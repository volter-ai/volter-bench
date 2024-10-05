from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
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
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        
        while True:
            # Player turn
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

            if choice == quit_button:
                self._reset_creatures()
                self._quit_whole_game()

            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Bot turn
            bot_skill = self._wait_for_choice(self.bot, [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolve turn
            self._resolve_turn(self.player, self.player_creature, player_skill, self.bot, self.bot_creature)
            if self._check_battle_end():
                break
            self._resolve_turn(self.bot, self.bot_creature, bot_skill, self.player, self.player_creature)
            if self._check_battle_end():
                break

    def _resolve_turn(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = skill.damage
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} fainted! You win!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
