from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}

> Use Skill
> Quit
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_turn()
            
            # Foe Choice Phase
            foe_skill = self.foe_turn()
            
            # Resolution Phase
            self.resolve_turn(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self.reset_creatures_state()
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, skill_choices).thing

    def foe_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, skill_choices).thing

    def resolve_turn(self, player_skill, foe_skill):
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.opponent, f"Opponent's {self.player_creature.display_name} used {player_skill.display_name}!")

        self.player_creature.hp -= foe_skill.damage
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {foe_skill.display_name}!")
        self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} used {foe_skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
