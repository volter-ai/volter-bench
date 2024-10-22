from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Player's turn:
> {self.player_creature.skills[0].display_name}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            if self.check_battle_end():
                self.handle_battle_end()
                break

    def player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if not self.check_battle_end():
                self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
            if not self.check_battle_end():
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
        else:
            # If speeds are equal, randomly choose who goes first
            first_attacker, first_creature, first_skill, first_defender, first_defender_creature = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature),
                (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
            ])
            second_attacker, second_creature, second_skill, second_defender, second_defender_creature = (
                (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
                if first_attacker == self.player else
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            )

            self.execute_skill(first_attacker, first_creature, first_skill, first_defender, first_defender_creature)
            if not self.check_battle_end():
                self.execute_skill(second_attacker, second_creature, second_skill, second_defender, second_defender_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self) -> bool:
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
