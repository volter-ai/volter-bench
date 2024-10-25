from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.reset_battle()

    def reset_battle(self):
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            self.reset_battle()
            self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
            
            while True:
                # Player Choice Phase
                player_skill = self.player_turn()
                
                # Foe Choice Phase
                opponent_skill = self.opponent_turn()
                
                # Resolution Phase
                self.resolve_turn(player_skill, opponent_skill)
                
                if self.check_battle_end():
                    break
            
            # Ask if the player wants to play again or quit
            play_again_button = Button("Play Again")
            quit_button = Button("Quit")
            choices = [play_again_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if quit_button == choice:
                self._transition_to_scene("MainMenuScene")
                return

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.opponent_creature.hp = max(0, self.opponent_creature.hp - player_skill.damage)
        self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")
        
        if self.opponent_creature.hp > 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp = max(0, self.player_creature.hp - opponent_skill.damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False
