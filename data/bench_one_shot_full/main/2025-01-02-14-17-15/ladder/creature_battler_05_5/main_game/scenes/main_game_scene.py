from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name}
Opponent: {self.opponent.display_name}
Active Creature: {self.opponent.active_creature.display_name}
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

    def player_choice_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.player, choices)

        if attack_button == choice:
            self.attack_phase(self.player)
        elif swap_button == choice:
            self.swap_phase(self.player)

    def foe_choice_phase(self):
        # Simulate bot choice
        self.attack_phase(self.opponent)

    def resolution_phase(self):
        # Resolve actions
        pass

    def attack_phase(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        chosen_skill = self._wait_for_choice(player, skill_choices)
        # Add logic to queue and resolve skill

    def swap_phase(self, player: Player):
        creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in creatures]
        chosen_creature = self._wait_for_choice(player, creature_choices)
        player.active_creature = chosen_creature
