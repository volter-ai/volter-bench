from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        self.battle_loop()
        self._handle_battle_end()

    def battle_loop(self):
        while not self._check_battle_end():
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, opponent_skill)

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = self.player, self.opponent
            first_skill, second_skill = player_skill, opponent_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = self.opponent, self.player
            first_skill, second_skill = opponent_skill, player_skill
        else:
            # Randomly determine who goes first when speeds are equal
            if random.choice([True, False]):
                first, second = self.player, self.opponent
                first_skill, second_skill = player_skill, opponent_skill
            else:
                first, second = self.opponent, self.player
                first_skill, second_skill = opponent_skill, player_skill

        self._execute_skill(first, first.creatures[0], first_skill, second, second.creatures[0])
        if second.creatures[0].hp > 0:
            self._execute_skill(second, second.creatures[0], second_skill, first, first.creatures[0])

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")

    def _check_battle_end(self) -> bool:
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
        
        # Ask the player if they want to play again or quit
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [play_again_button, quit_button])
        
        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
