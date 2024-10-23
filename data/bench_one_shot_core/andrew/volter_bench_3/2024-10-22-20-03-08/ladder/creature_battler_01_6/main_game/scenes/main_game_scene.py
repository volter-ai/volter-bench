from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.player_skill_queue = []
        self.foe_skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            if self.player_choice_phase():
                self._quit_whole_game()
                return

            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                return

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if use_skill_button == choice:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_skill_queue.append(skill_choice.thing)
            return False
        elif quit_button == choice:
            return True

    def foe_choice_phase(self):
        foe_skill = self.foe_creature.skills[0]  # Bot always uses the first skill
        self.foe_skill_queue.append(foe_skill)

    def resolution_phase(self):
        player_skill = self.player_skill_queue.pop(0)
        foe_skill = self.foe_skill_queue.pop(0)

        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.foe_creature.hp -= player_skill.damage
        self.foe_creature.hp = max(0, self.foe_creature.hp)

        if self.foe_creature.hp > 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} used {foe_skill.display_name}!")
            self.player_creature.hp -= foe_skill.damage
            self.player_creature.hp = max(0, self.player_creature.hp)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
