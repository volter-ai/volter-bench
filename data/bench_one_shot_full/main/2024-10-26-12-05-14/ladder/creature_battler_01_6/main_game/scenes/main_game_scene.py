from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.description}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            self.skill_queue.append(player_skill)

            # Foe Choice Phase
            self._show_text(self.foe, f"It's your turn, {self.foe.display_name}!")
            foe_skill = self._player_choice_phase(self.foe, self.foe_creature)
            self.skill_queue.append(foe_skill)

            # Resolution Phase
            self._resolve_skills()

            if self._check_battle_end():
                self._reset_creatures()
                break

    def _player_choice_phase(self, current_player, current_creature):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(current_player, [use_skill_button, quit_button])

        if quit_button == choice:
            self._reset_creatures()
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in current_creature.skills]
        return self._wait_for_choice(current_player, skill_choices).thing

    def _resolve_skills(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                self._apply_damage(self.foe_creature, skill.damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name}!")
                self._show_text(self.foe, f"Opponent's {self.player_creature.display_name} used {skill.display_name}!")
            else:
                self._apply_damage(self.player_creature, skill.damage)
                self._show_text(self.foe, f"Your {self.foe_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Opponent's {self.foe_creature.display_name} used {skill.display_name}!")

    def _apply_damage(self, creature, damage):
        creature.hp = max(0, creature.hp - damage)

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp

    def _transition_to_scene(self, scene_name: str):
        self._reset_creatures()
        super()._transition_to_scene(scene_name)
