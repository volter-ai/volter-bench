from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature, Skill
from typing import List, Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Tuple[Creature, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            self.skill_queue.append((self.player_creature, player_skill))
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            self.skill_queue.append((self.foe_creature, foe_skill))
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            defender = self.foe_creature if attacker == self.player_creature else self.player_creature
            defender.hp -= skill.damage
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.foe, f"{attacker.display_name} used {skill.display_name}!")
            
            if defender.hp <= 0:
                break

    def check_battle_end(self) -> bool:
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.foe.creatures:
            creature.hp = creature.max_hp
