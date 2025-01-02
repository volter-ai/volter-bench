from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    TYPE_EFFECTIVENESS = {
        "normal": {},
        "fire": {"leaf": 2, "water": 0.5},
        "water": {"fire": 2, "leaf": 0.5},
        "leaf": {"water": 2, "fire": 0.5}
    }

    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Your Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

    def player_choice_phase(self):
        creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        self.foe_choice = self._wait_for_choice(self.opponent, choices)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
        else:
            self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        effectiveness = self.TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1)
        final_damage = max(0, int(raw_damage * effectiveness))  # Ensure damage is not negative
        defender.hp -= final_damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {final_damage} damage!")

    def end_battle(self):
        if self.player.creatures[0].hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._quit_whole_game()
