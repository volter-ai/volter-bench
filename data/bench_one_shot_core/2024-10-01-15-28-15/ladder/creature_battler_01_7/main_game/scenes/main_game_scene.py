import time
from collections import deque

from main_game.models import Player
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Opponent: {self.opponent.display_name}\n"
            f"Opponent's Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})\n"
        )

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            self.player_choice_phase()
            self.foe_choice_phase()

            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_creatures()
        
        self._show_text(self.player, "Returning to the main menu...")
        self._show_text(self.opponent, "Returning to the main menu...")
        time.sleep(2)
        
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.skill_queue.append((self.opponent, choice.thing))

    def resolution_phase(self):
        while self.skill_queue:
            acting_player, skill = self.skill_queue.popleft()
            if acting_player == self.player:
                target = self.opponent_creature
                self._show_text(self.player, f"You used {skill.display_name}!")
                self._show_text(self.opponent, f"Opponent used {skill.display_name}!")
            else:
                target = self.player_creature
                self._show_text(self.player, f"Opponent used {skill.display_name}!")
                self._show_text(self.opponent, f"You used {skill.display_name}!")

            target.hp -= skill.damage
            target.hp = max(0, target.hp)

            if self.check_battle_end():
                break

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self.skill_queue.clear()
