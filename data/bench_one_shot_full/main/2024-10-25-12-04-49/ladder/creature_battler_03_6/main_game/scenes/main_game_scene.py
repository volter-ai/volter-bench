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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player turn
            player_skill = self.player_choice_phase()
            
            # Opponent turn
            opponent_skill = self.opponent_choice_phase()
            
            # Resolution phase
            self.resolution_phase(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def determine_first_attacker(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.player_creature
        elif self.opponent_creature.speed > self.player_creature.speed:
            return self.opponent, self.opponent_creature
        else:
            # Speed tie, choose randomly
            return random.choice([(self.player, self.player_creature), (self.opponent, self.opponent_creature)])

    def resolution_phase(self, player_skill, opponent_skill):
        first_attacker, first_creature = self.determine_first_attacker()
        second_attacker = self.opponent if first_attacker == self.player else self.player
        second_creature = self.opponent_creature if first_creature == self.player_creature else self.player_creature

        first_skill = player_skill if first_attacker == self.player else opponent_skill
        second_skill = opponent_skill if first_attacker == self.player else player_skill

        self.execute_skill(first_attacker, first_creature, first_skill, second_creature)
        if second_creature.hp > 0:
            self.execute_skill(second_attacker, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * weakness_factor)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self.end_battle()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self.end_battle()
            return True
        return False

    def end_battle(self):
        play_again = Button("Play Again")
        quit_game = Button("Quit Game")
        choice = self._wait_for_choice(self.player, [play_again, quit_game])
        
        if choice == play_again:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
