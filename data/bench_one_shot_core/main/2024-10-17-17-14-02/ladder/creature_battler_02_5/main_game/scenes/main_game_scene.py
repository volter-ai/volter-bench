import random
from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player Choice Phase
            player_skill = self._player_turn()
            
            # Foe Choice Phase
            foe_skill = self._foe_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, foe_skill)
            
            if self._check_battle_end():
                break

        # After the battle ends, show options to play again or quit
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if play_again_button == choice:
            self._transition_to_scene("MainMenuScene")
        elif quit_button == choice:
            self._quit_whole_game()

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self, player_skill, foe_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Random order resolution when speeds are equal
            first_attacker, first_creature, first_skill, second_attacker, second_creature, second_skill = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill),
                (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
            ])
            self._execute_skill(first_attacker, first_creature, first_skill, second_creature)
            if second_creature.hp > 0:
                self._execute_skill(second_attacker, second_creature, second_skill, first_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} takes {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
