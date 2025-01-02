from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

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
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            # Player Choice Phase
            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])

            # Foe Choice Phase
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            # Resolution Phase
            self.resolve_turn(player_creature, opponent_creature, player_choice.thing, opponent_choice.thing)

            # Check for end of battle
            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self.end_battle(player_creature, opponent_creature)
                break

    def resolve_turn(self, player_creature, opponent_creature, player_skill, opponent_skill):
        # Determine turn order based on speed
        creatures = [(player_creature, player_skill), (opponent_creature, opponent_skill)]
        creatures.sort(key=lambda x: x[0].speed, reverse=True)

        if creatures[0][0].speed == creatures[1][0].speed:
            random.shuffle(creatures)

        # Execute skills in order
        for creature, skill in creatures:
            target = opponent_creature if creature == player_creature else player_creature
            self.execute_skill(creature, target, skill)

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense

        # Calculate type effectiveness
        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = max(0, int(raw_damage * type_effectiveness))

        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)

    def get_type_effectiveness(self, skill_type, creature_type):
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def end_battle(self, player_creature, opponent_creature):
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")

        # Offer choice to return to main menu or quit
        return_to_menu_button = Button("Return to Main Menu")
        quit_button = Button("Quit Game")
        choice = self._wait_for_choice(self.player, [return_to_menu_button, quit_button])

        if choice == return_to_menu_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
