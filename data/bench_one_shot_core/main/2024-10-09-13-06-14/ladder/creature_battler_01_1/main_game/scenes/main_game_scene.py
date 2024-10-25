from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from collections import deque


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue = deque()

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
        while True:
            if self._check_battle_end():
                break

            self._player_choice_phase()
            self._foe_choice_phase()
            self._resolution_phase()

    def _player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == quit_button:
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        self.skill_queue.append((self.player, skill_choice.thing))

    def _foe_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        self.skill_queue.append((self.opponent, skill_choice.thing))

    def _resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.popleft()
            defender = self.opponent if attacker == self.player else self.player
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name}!")

            defender_creature.hp -= skill.damage

            self._show_text(self.player, f"{defender.display_name}'s creature took {skill.damage} damage!")
            self._show_text(self.opponent, f"{defender.display_name}'s creature took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
