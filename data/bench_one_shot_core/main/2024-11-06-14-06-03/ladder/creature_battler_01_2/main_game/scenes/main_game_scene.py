from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


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
{', '.join([skill.display_name for skill in self.player_creature.skills])}

> Use Skill
> Quit
"""

    def run(self):
        while True:
            # Player turn
            self._show_text(self.player, "Your turn!")
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choices = [use_skill_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if quit_button == choice:
                self._quit_whole_game()

            if use_skill_button == choice:
                skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                self.apply_skill(self.player_creature, self.opponent_creature, skill_choice.thing)

            if self.check_battle_end():
                break

            # Opponent turn
            self._show_text(self.opponent, "Opponent's turn!")
            opponent_skill = self.opponent_creature.skills[0]  # Simple AI: always use the first skill
            self.apply_skill(self.opponent_creature, self.player_creature, opponent_skill)

            if self.check_battle_end():
                break

    def apply_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        defender.hp = max(0, defender.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name}!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
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
        self._show_text(self.player, "All creatures have been restored to full health.")
        self._show_text(self.opponent, "All creatures have been restored to full health.")
