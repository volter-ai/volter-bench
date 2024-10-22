import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


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

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
            self.battle_loop()
            
            play_again = self.ask_play_again()
            if not play_again:
                break

            # Reset creatures for a new battle
            self.player_creature.hp = self.player_creature.max_hp
            self.opponent_creature.hp = self.opponent_creature.max_hp

        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            # Player turn
            player_skill = self.choose_skill(self.player, self.player_creature)
            
            # Opponent turn
            opponent_skill = self.choose_skill(self.opponent, self.opponent_creature)
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def choose_skill(self, actor: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return choice.thing

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
        else:
            # Equal speeds, randomly decide who goes first
            first_attacker, first_creature, first_skill, second_attacker, second_creature, second_skill = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, opponent_skill),
                (self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature, player_skill)
            ])
            
            self.execute_skill(first_attacker, first_creature, first_skill, second_attacker, second_creature)
            if second_creature.hp > 0:
                self.execute_skill(second_attacker, second_creature, second_skill, first_attacker, first_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def ask_play_again(self) -> bool:
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)
        return choice == play_again_button
