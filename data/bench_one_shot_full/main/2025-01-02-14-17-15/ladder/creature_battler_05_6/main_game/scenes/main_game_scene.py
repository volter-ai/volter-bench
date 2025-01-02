from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Opponent: {self.opponent.display_name}
Active Creature: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

Choose your action:
1. Attack
2. Swap
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
            self.choose_skill(self.player)
        elif choice == swap_button:
            self.choose_swap(self.player)

    def foe_choice_phase(self):
        if random.choice([True, False]):
            self.choose_skill(self.opponent)
        else:
            self.choose_swap(self.opponent)

    def resolution_phase(self):
        # Implement the logic to resolve the queued actions
        pass

    def choose_skill(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        chosen_skill = self._wait_for_choice(player, skill_choices)
        # Queue the chosen skill for resolution
        pass

    def choose_swap(self, player: Player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        chosen_creature = self._wait_for_choice(player, creature_choices)
        player.active_creature = chosen_creature.thing

    def check_battle_end(self):
        if all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp <= 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
