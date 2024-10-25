from mini_game_engine.engine.lib import AbstractGameScene, Button


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
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            battle_ended, winner = self._check_battle_end()
            if battle_ended:
                self._show_battle_result(winner)
                self._handle_post_battle()
                break

    def _player_choice_phase(self, current_player, current_creature):
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        self._apply_damage(self.opponent_creature, player_skill)
        self._apply_damage(self.player_creature, foe_skill)

    def _apply_damage(self, target, skill):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{skill.display_name} deals {skill.damage} damage to {target.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            return True, self.opponent
        elif self.opponent_creature.hp == 0:
            return True, self.player
        return False, None

    def _show_battle_result(self, winner):
        if winner == self.player:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")

    def _handle_post_battle(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
