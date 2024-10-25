from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_result = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appeared!")
        self.battle_loop()
        self.display_battle_result()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.check_battle_end():
                break

        self.reset_creatures()

    def player_choice_phase(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self.opponent_creature.hp = max(0, self.opponent_creature.hp)

        self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
        self.player_creature.hp -= opponent_skill.damage
        self.player_creature.hp = max(0, self.player_creature.hp)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self.battle_result = "lose"
            return True
        elif self.opponent_creature.hp == 0:
            self.battle_result = "win"
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def display_battle_result(self):
        if self.battle_result == "win":
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted. You win!")
        elif self.battle_result == "lose":
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
        self._show_text(self.player, "Returning to the main menu...")
