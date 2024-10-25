from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue: List[tuple[Creature, Skill]] = []

    def __str__(self):
        skills_str = "\n".join([f"{i+1}. {skill.display_name}" for i, skill in enumerate(self.player_creature.skills)])
        return (
            f"Battle!\n"
            f"Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}\n"
            f"Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}\n"
            f"Available skills:\n{skills_str}\n"
            f"{len(self.player_creature.skills) + 1}. Quit"
        )

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()
            if player_skill is None:
                return

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()

            # Add skills to the queue
            self.skill_queue.append((self.player_creature, player_skill))
            self.skill_queue.append((self.opponent_creature, foe_skill))

            # Resolution Phase
            self._resolution_phase()

            if self._check_battle_end():
                return

    def _player_choice_phase(self) -> Skill | None:
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choices.append(Button("Quit"))
        choice = self._wait_for_choice(self.player, choices)

        if choice.display_name == "Quit":
            self._transition_to_scene("MainMenuScene")
            return None
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        foe_skill = next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)
        self._show_text(self.player, f"Opponent chose {foe_skill.display_name}!")
        return foe_skill

    def _resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            defender.hp = max(0, defender.hp - skill.damage)
            self._show_text(self.player, f"{defender.display_name} took {skill.damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self.skill_queue.clear()
