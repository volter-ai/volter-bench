from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
{self._get_skill_choices_str(self.player_creature)}
"""

    def _get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            opponent_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, opponent_skill)
            
            if self._check_battle_end():
                break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        player_first = self._determine_first_attacker()
        
        if player_first:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if not self._check_battle_end():
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
        else:
            self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
            if not self._check_battle_end():
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)

    def _determine_first_attacker(self) -> bool:
        if self.player_creature.speed > self.opponent_creature.speed:
            return True
        elif self.player_creature.speed < self.opponent_creature.speed:
            return False
        else:
            return random.choice([True, False])

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Ensure HP doesn't go below 0
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
