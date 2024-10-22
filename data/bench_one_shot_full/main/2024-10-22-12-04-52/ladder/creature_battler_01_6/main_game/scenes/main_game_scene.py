from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        while True:
            self._show_text(self.player, "A wild opponent appears!")
            battle_result = self._run_battle()
            
            if battle_result == "win":
                self._show_text(self.player, "You won the battle!")
            else:
                self._show_text(self.player, "You lost the battle!")

            self._reset_creatures()

            play_again = self._ask_play_again()
            if not play_again:
                self._transition_to_scene("MainMenuScene")
                return

    def _run_battle(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)
            
            if self._check_battle_end():
                if self.player_creature.hp <= 0:
                    return "lose"
                elif self.opponent_creature.hp <= 0:
                    return "win"

    def _player_choice_phase(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, opponent_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.opponent, f"Opponent used {opponent_skill.display_name}!")
        
        self.opponent_creature.hp -= player_skill.damage
        self.player_creature.hp -= opponent_skill.damage
        
        self._show_text(self.player, f"You dealt {player_skill.damage} damage!")
        self._show_text(self.player, f"You received {opponent_skill.damage} damage!")

    def _check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def _ask_play_again(self):
        play_again_button = Button("Play Again")
        main_menu_button = Button("Return to Main Menu")
        choice = self._wait_for_choice(self.player, [play_again_button, main_menu_button])
        return choice == play_again_button
