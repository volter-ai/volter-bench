from typing import List

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[tuple[Creature, Skill]] = []

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
            self.skill_queue.clear()
            
            # Player Choice Phase
            self.player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            self.player_choice_phase(self.foe, self.foe_creature)
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self, player: Player, creature: Creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        chosen_skill = next(skill for skill in creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append((creature, chosen_skill))

    def resolution_phase(self):
        for creature, skill in self.skill_queue:
            if creature == self.player_creature:
                target = self.foe_creature
            else:
                target = self.player_creature
            
            target.hp -= skill.damage
            self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
            self._show_text(self.foe, f"{creature.display_name} used {skill.display_name}!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
