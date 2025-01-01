from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""===Main Game===
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

    def player_choice_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == attack_button:
            self.attack_phase(self.player)
        elif choice == swap_button:
            self.swap_phase(self.player)

    def foe_choice_phase(self):
        # Simulate bot choice
        self.attack_phase(self.opponent)

    def attack_phase(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        chosen_skill = self._wait_for_choice(player, skill_choices)
        # Add logic to queue the chosen skill for resolution

    def swap_phase(self, player: Player):
        creatures = [creature for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        creature_choices = [SelectThing(creature) for creature in creatures]
        chosen_creature = self._wait_for_choice(player, creature_choices)
        player.active_creature = chosen_creature

    def resolution_phase(self):
        # Resolve queued actions
        pass
