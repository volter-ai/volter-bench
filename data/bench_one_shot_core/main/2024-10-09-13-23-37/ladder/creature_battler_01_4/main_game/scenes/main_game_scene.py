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
            # Clear the skill queue at the start of each turn
            self.skill_queue.clear()

            # Player Choice Phase
            self.queue_skill(self.player, self.player_creature)

            # Foe Choice Phase
            self.queue_skill(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolve_skills()

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")  # Return to the main menu after the battle

    def queue_skill(self, current_player: Player, current_creature: Creature):
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        self.skill_queue.append((current_player, current_creature, choice.thing))

    def resolve_skills(self):
        for player, creature, skill in self.skill_queue:
            if player == self.player:
                target_creature = self.opponent_creature
                target_player = self.opponent
            else:
                target_creature = self.player_creature
                target_player = self.player

            target_creature.hp = max(0, target_creature.hp - skill.damage)
            self._show_text(player, f"Your {creature.display_name} used {skill.display_name}!")
            self._show_text(target_player, f"Opponent's {creature.display_name} used {skill.display_name}!")

            if self.check_battle_end():
                break

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
