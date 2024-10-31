from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue: List[tuple[Player, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Queued skills: {', '.join([skill.display_name for _, skill in self.skill_queue])}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            if not self._player_turn():
                return

            # Opponent turn
            self._opponent_turn()

            # Resolution phase
            self._resolve_turn()

            if self._check_battle_end():
                self._reset_creatures()
                return

    def _player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

        if choice == quit_button:
            self._reset_creatures()
            self._quit_whole_game()
            return False

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        self.skill_queue.append((self.player, skill_choice.thing))
        return True

    def _opponent_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        self.skill_queue.append((self.opponent, skill_choice.thing))

    def _resolve_turn(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            if attacker == self.player:
                target = self.opponent_creature
            else:
                target = self.player_creature
            self._apply_damage(attacker, skill, target)

    def _apply_damage(self, attacker, skill, target):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{target.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self.skill_queue.clear()
