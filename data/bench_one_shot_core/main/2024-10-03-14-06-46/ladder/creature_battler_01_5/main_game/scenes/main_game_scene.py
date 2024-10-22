from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
> Use Skill
> Quit
"""

    def run(self):
        while True:
            # Player Choice Phase
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choices = [use_skill_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if quit_button == choice:
                self._quit_whole_game()

            if use_skill_button == choice:
                skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
                player_skill = self._wait_for_choice(self.player, skill_choices).thing

                # Foe Choice Phase
                foe_skill_choices = [SelectThing(skill) for skill in self.foe_creature.skills]
                foe_skill = self._wait_for_choice(self.foe, foe_skill_choices).thing

                # Resolution Phase
                self._resolve_skills(player_skill, foe_skill)

            if self._check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def _resolve_skills(self, player_skill: Skill, foe_skill: Skill):
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.foe, f"Opponent's {self.player_creature.display_name} used {player_skill.display_name}!")

        self.player_creature.hp -= foe_skill.damage
        self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")
        self._show_text(self.foe, f"Your {self.foe_creature.display_name} used {foe_skill.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False
