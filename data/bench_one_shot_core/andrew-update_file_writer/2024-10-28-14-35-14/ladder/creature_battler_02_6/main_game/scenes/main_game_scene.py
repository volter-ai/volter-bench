from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            # Check for battle end
            battle_ended, player_won = self._check_battle_end()
            if battle_ended:
                self._end_game(player_won)
                break

    def _player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, foe_skill):
        first, second = self._determine_order()
        self._execute_skill(first, second, player_skill if first == self.player else foe_skill)
        if not self._check_battle_end()[0]:
            self._execute_skill(second, first, foe_skill if first == self.player else player_skill)

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def _execute_skill(self, attacker, defender, skill):
        attacker_creature = attacker.creatures[0]
        defender_creature = defender.creatures[0]
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            return True, False  # Battle ended, player lost
        elif self.opponent_creature.hp <= 0:
            return True, True  # Battle ended, player won
        return False, False  # Battle not ended

    def _end_game(self, player_won):
        if player_won:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
        else:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")

        # Ask the player if they want to play again or quit
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [play_again_button, quit_button])

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
