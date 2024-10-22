import random
from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature


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
{self._get_skill_choices_str()}
"""

    def _get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self, player: Player, creature: Creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent: Player, creature: Creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed == self.opponent_creature.speed:
            # If speeds are equal, randomly decide who goes first
            first_attacker = random.choice([self.player, self.opponent])
            if first_attacker == self.player:
                first, second = (self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, foe_skill)
            else:
                first, second = (self.opponent, self.opponent_creature, foe_skill), (self.player, self.player_creature, player_skill)
        elif self.player_creature.speed > self.opponent_creature.speed:
            first, second = (self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, foe_skill)
        else:
            first, second = (self.opponent, self.opponent_creature, foe_skill), (self.player, self.player_creature, player_skill)

        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender, defender_creature = self.opponent, self.opponent_creature
            else:
                defender, defender_creature = self.player, self.player_creature

            damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
            defender_creature.hp = max(0, defender_creature.hp - damage)

            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

            if defender_creature.hp == 0:
                break

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
