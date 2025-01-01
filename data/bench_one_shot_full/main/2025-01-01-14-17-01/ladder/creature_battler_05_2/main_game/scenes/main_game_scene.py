from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Bot: {self.bot.display_name}
Active Creature: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

Choose your action:
1. Attack
2. Swap
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
        # Bot logic for choosing attack or swap
        if self.bot.active_creature.hp < 10:
            self.swap_phase(self.bot)
        else:
            self.attack_phase(self.bot)

    def attack_phase(self, player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        chosen_skill = self._wait_for_choice(player, skill_choices)
        # Add chosen skill to action queue

    def swap_phase(self, player):
        creatures = [creature for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in creatures]
        chosen_creature = self._wait_for_choice(player, creature_choices)
        player.active_creature = chosen_creature

    def resolution_phase(self):
        # Resolve actions based on speed and type effectiveness
        pass
