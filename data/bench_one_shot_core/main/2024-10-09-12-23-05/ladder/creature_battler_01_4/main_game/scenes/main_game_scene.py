from typing import List, Tuple
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue: List[Tuple[Player, Creature, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self.player_choice_phase()

            # Foe Choice Phase
            self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase()

            if self.check_battle_end():
                break

            # Clear the skill queue for the next round
            self.skill_queue.clear()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        player_skill = self.choose_skill(self.player, self.player_creature)
        self.skill_queue.append((self.player, self.player_creature, player_skill))

    def foe_choice_phase(self):
        opponent_skill = self.choose_skill(self.opponent, self.opponent_creature)
        self.skill_queue.append((self.opponent, self.opponent_creature, opponent_skill))

    def resolution_phase(self):
        for attacker, attacker_creature, skill in self.skill_queue:
            defender = self.opponent if attacker == self.player else self.player
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

            defender_creature.hp = max(0, defender_creature.hp - skill.damage)
            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.opponent, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")

            if defender_creature.hp <= 0:
                break

    def choose_skill(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
