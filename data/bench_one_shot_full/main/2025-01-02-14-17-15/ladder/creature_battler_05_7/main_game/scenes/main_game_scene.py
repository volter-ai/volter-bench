from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Opponent: {self.opponent.display_name}
Active Creature: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == attack_button:
            skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
            selected_skill = self._wait_for_choice(self.player, skill_choices)
            self.player_action = selected_skill.thing
        elif choice == swap_button:
            swap_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
            selected_creature = self._wait_for_choice(self.player, swap_choices)
            self.player_action = selected_creature.thing

    def foe_choice_phase(self):
        self.opponent_action = random.choice(self.opponent.active_creature.skills)

    def resolution_phase(self):
        # Implement resolution logic based on player_action and opponent_action
        pass

    def check_battle_end(self):
        if self.player.active_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent.active_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
