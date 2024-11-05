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
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.damage} damage" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player turn
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

            if quit_button == choice:
                self._quit_whole_game()

            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Opponent turn
            opponent_skill = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)

            if self._check_battle_end():
                break

        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self, player_skill, opponent_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")

        if self.opponent_creature.hp > 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp -= opponent_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
