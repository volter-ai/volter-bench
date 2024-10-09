from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()
                self.handle_end_of_battle()
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self.opponent_creature.hp = max(0, self.opponent_creature.hp)

        self._show_text(self.player, f"Foe's {self.opponent_creature.display_name} used {foe_skill.display_name}!")
        self.player_creature.hp -= foe_skill.damage
        self.player_creature.hp = max(0, self.player_creature.hp)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Foe's {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def handle_end_of_battle(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
