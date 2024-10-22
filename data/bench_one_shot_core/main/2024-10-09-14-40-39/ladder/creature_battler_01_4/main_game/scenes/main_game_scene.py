from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, RandomModeGracefulExit


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while True:
            try:
                # Player Choice Phase
                player_skill = self._player_choice_phase()
                
                # Foe Choice Phase
                foe_skill = self._foe_choice_phase()
                
                # Resolution Phase
                self._resolution_phase(player_skill, foe_skill)
                
                # Check for battle end
                if self._check_battle_end():
                    break

            except RandomModeGracefulExit:
                self._transition_to_scene("MainMenuScene")
                return

        # Transition back to MainMenuScene after battle ends
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} (Damage: {skill.damage})") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} (Damage: {skill.damage})") for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, foe_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Foe's {self.foe_creature.display_name} took {player_skill.damage} damage!")

        if self.foe_creature.hp > 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {foe_skill.display_name}!")
            self.player_creature.hp -= foe_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {foe_skill.damage} damage!")

    def _check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} fainted! You win!")
            self._reset_creatures()
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            self._reset_creatures()
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
