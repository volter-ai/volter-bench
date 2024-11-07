from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        battle_ended = False
        while not battle_ended:
            # Player Choice Phase
            player_skill = self._player_turn()
            
            # Foe Choice Phase
            opponent_skill = self._opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            battle_ended = self._check_battle_end()

        self._end_battle()

    def _player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skills(self.player, self.player_creature, player_skill, 
                                 self.opponent, self.opponent_creature, opponent_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            self._execute_skills(self.opponent, self.opponent_creature, opponent_skill, 
                                 self.player, self.player_creature, player_skill)
        else:
            # Equal speed: randomly decide who goes first
            if random.choice([True, False]):
                self._show_text(self.player, "Speed tie! You go first!")
                self._execute_skills(self.player, self.player_creature, player_skill, 
                                     self.opponent, self.opponent_creature, opponent_skill)
            else:
                self._show_text(self.player, "Speed tie! Opponent goes first!")
                self._execute_skills(self.opponent, self.opponent_creature, opponent_skill, 
                                     self.player, self.player_creature, player_skill)

    def _execute_skills(self, first_player, first_creature, first_skill, 
                        second_player, second_creature, second_skill):
        self._execute_skill(first_player, first_creature, first_skill, second_creature)
        if second_creature.hp > 0:
            self._execute_skill(second_player, second_creature, second_skill, first_creature)

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} takes {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0:
            return True
        return False

    def _end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")

        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
