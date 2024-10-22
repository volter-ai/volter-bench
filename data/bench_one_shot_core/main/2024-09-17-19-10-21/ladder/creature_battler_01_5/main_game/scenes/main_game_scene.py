from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.game_over = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while not self.game_over:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)
            self.check_battle_end()

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")

        if self.opponent_creature.hp > 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp -= opponent_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.game_over = True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.game_over = True
