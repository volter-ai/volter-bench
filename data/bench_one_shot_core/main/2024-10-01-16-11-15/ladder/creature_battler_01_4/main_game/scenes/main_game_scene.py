from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.player_skill = None
        self.foe_skill = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices()}
"""

    def get_skill_choices(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.foe_skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {self.player_skill.display_name}!")
        self.foe_creature.hp -= self.player_skill.damage
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} used {self.foe_skill.display_name}!")
        self.player_creature.hp -= self.foe_skill.damage

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.foe_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
        else:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
        
        self.reset_creatures()
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
