from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill_queue = []
        self.opponent_skill_queue = []
        self.player_skill_selected = False
        self.opponent_skill_selected = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            if self._check_battle_end():
                break

            if not self.player_skill_selected:
                self._player_turn()
            if not self.opponent_skill_selected:
                self._opponent_turn()
            
            if self.player_skill_selected and self.opponent_skill_selected:
                self._resolve_turn()
                self.player_skill_selected = False
                self.opponent_skill_selected = False

    def _player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if use_skill_button == choice:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_skill_queue.append(skill_choice.thing)
            self.player_skill_selected = True
        elif quit_button == choice:
            self._quit_whole_game()

    def _opponent_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        self.opponent_skill_queue.append(skill_choice.thing)
        self.opponent_skill_selected = True

    def _resolve_turn(self):
        player_skill = self.player_skill_queue.pop(0)
        opponent_skill = self.opponent_skill_queue.pop(0)

        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")

        if not self._check_battle_end():
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp -= opponent_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
