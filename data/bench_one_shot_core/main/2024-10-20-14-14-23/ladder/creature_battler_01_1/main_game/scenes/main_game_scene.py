from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        return "\n".join([f"- {skill.display_name}: {skill.description}" for skill in skills])

    def run(self):
        self.reset_creatures()  # Reset creatures when entering the scene
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end condition
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        return skill_choice.thing

    def foe_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        return skill_choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self.opponent_creature.hp = max(0, self.opponent_creature.hp)

        self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} used {foe_skill.display_name}!")
        self.player_creature.hp -= foe_skill.damage
        self.player_creature.hp = max(0, self.player_creature.hp)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self.reset_creatures()  # Reset creatures before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self.reset_creatures()  # Reset creatures before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
