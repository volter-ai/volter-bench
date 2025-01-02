from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
from mini_game_engine.engine.lib import Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Battle ===
Player: {player_creature.display_name} (HP: {player_creature.hp})
Opponent: {opponent_creature.display_name} (HP: {opponent_creature.hp})

Choose a skill:
"""

    def run(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self._show_text(self.player, "Battle Over!")
                self.end_battle()
                break

            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            self.resolve_turn(player_creature, opponent_creature, player_choice.thing, opponent_choice.thing)

    def resolve_turn(self, player_creature: Creature, opponent_creature: Creature, player_skill: Skill, opponent_skill: Skill):
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_skill)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            self.execute_skill(opponent_creature, player_creature, opponent_skill)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_skill)
        else:
            # Randomly decide which creature goes first if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, player_skill)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, opponent_skill)
            else:
                self.execute_skill(opponent_creature, player_creature, opponent_skill)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, player_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp -= damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")

    def end_battle(self):
        # Offer the player a choice to return to the main menu or quit the game
        return_to_menu_button = Button("Return to Main Menu")
        quit_button = Button("Quit Game")
        choices = [return_to_menu_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == return_to_menu_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
