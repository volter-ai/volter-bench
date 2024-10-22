from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill_queue = []
        self.opponent_skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        while True:
            if self.player_choice_phase() and self.foe_choice_phase():
                if not self.resolution_phase():
                    break
            else:
                break
        self.handle_battle_end()

    def player_choice_phase(self):
        self._show_text(self.player, "Your turn!")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.player_skill_queue.append(selected_skill)
        return True

    def foe_choice_phase(self):
        self._show_text(self.opponent, "Opponent's turn!")
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        selected_skill = next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)
        self.opponent_skill_queue.append(selected_skill)
        return True

    def resolution_phase(self):
        player_skill = self.player_skill_queue.pop(0)
        opponent_skill = self.opponent_skill_queue.pop(0)

        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        if self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} wins!")
            return False

        self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} uses {opponent_skill.display_name}!")
        self.player_creature.hp -= opponent_skill.damage
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name} wins!")
            return False

        return True

    def handle_battle_end(self):
        self._show_text(self.player, "Battle has ended!")
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if play_again_button == choice:
            self._transition_to_scene("MainMenuScene")
        elif quit_button == choice:
            self._quit_whole_game()
