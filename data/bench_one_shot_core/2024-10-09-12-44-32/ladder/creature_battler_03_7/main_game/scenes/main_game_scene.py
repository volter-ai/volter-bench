import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        if self.battle_ended:
            return """===Battle Ended===
1. Return to Main Menu
2. Quit Game
"""
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            if self.battle_ended:
                self._handle_post_battle()
                if self.battle_ended:  # If still true, it means the player chose to quit
                    self._quit_whole_game()
                break

            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turn
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self.battle_ended = True

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # Equal speeds, randomly choose who goes first
            first_attacker, first_defender, first_skill = random.choice([
                (self.player_creature, self.opponent_creature, player_skill),
                (self.opponent_creature, self.player_creature, opponent_skill)
            ])
            second_attacker, second_defender, second_skill = (
                (self.player_creature, self.opponent_creature, player_skill)
                if first_attacker == self.opponent_creature
                else (self.opponent_creature, self.player_creature, opponent_skill)
            )
            
            self._execute_skill(first_attacker, first_defender, first_skill)
            if first_defender.hp > 0:
                self._execute_skill(second_attacker, second_defender, second_skill)

    def _execute_skill(self, attacker, defender, skill):
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_factor(self, skill_type, defender_type):
        if skill_type == "fire" and defender_type == "leaf":
            return 2.0
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "fire":
            return 2.0
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "water":
            return 2.0
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _handle_post_battle(self):
        return_to_menu = Button("Return to Main Menu")
        quit_game = Button("Quit Game")
        choices = [return_to_menu, quit_game]
        choice = self._wait_for_choice(self.player, choices)

        if choice == return_to_menu:
            self._transition_to_scene("MainMenuScene")
            self.battle_ended = False
        elif choice == quit_game:
            self.battle_ended = True
