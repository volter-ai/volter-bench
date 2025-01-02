from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}
"""

    def run(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
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
            skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            # Add skill_choice to action queue
        elif choice == swap_button:
            creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
            creature_choice = self._wait_for_choice(self.player, creature_choices)
            # Swap creature

    def foe_choice_phase(self):
        # Similar logic for bot choice
        pass

    def resolution_phase(self):
        # Resolve actions
        pass
