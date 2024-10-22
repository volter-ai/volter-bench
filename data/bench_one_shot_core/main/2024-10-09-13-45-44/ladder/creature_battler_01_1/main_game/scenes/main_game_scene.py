from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.player_skill_queue = []
        self.foe_skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                self.post_battle_menu()
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.foe_skill_queue.append(choice.thing)

    def resolution_phase(self):
        player_skill = self.player_skill_queue.pop(0)
        foe_skill = self.foe_skill_queue.pop(0)

        self._show_text(self.player, f"{self.player_creature.display_name} used {player_skill.display_name}!")
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.foe_creature.display_name} took {player_skill.damage} damage!")

        if self.foe_creature.hp > 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")
            self.player_creature.hp -= foe_skill.damage
            self._show_text(self.player, f"{self.player_creature.display_name} took {foe_skill.damage} damage!")

    def check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"You won! {self.foe_creature.display_name} fainted!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"You lost! {self.player_creature.display_name} fainted!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp

    def post_battle_menu(self):
        self.reset_creatures()
        return_button = Button("Return to Main Menu")
        quit_button = Button("Quit Game")
        choices = [return_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == return_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
