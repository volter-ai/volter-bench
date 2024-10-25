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
{', '.join([skill.display_name for skill in self.player_creature.skills])}

> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self.player_turn()
            if player_skill is None:  # Player chose to quit
                self.reset_creatures_state()
                return

            # Opponent turn
            opponent_skill = self.opponent_turn()

            # Resolution phase
            self.resolve_turn(player_skill, opponent_skill)

            if self.check_battle_end():
                self.reset_creatures_state()
                return

    def player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()
            return None

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        return skill_choice.thing

    def opponent_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        return skill_choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")

        if self.opponent_creature.hp > 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp -= opponent_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def check_battle_end(self):
        if self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
