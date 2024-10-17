from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turns
            self._resolve_turns(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._end_battle()
                break

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turns(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first_attacker, first_skill, first_defender = self.player_creature, player_skill, self.opponent_creature
            second_attacker, second_skill, second_defender = self.opponent_creature, opponent_skill, self.player_creature
        elif self.player_creature.speed < self.opponent_creature.speed:
            first_attacker, first_skill, first_defender = self.opponent_creature, opponent_skill, self.player_creature
            second_attacker, second_skill, second_defender = self.player_creature, player_skill, self.opponent_creature
        else:
            # If speeds are equal, randomly choose who goes first
            if random.choice([True, False]):
                first_attacker, first_skill, first_defender = self.player_creature, player_skill, self.opponent_creature
                second_attacker, second_skill, second_defender = self.opponent_creature, opponent_skill, self.player_creature
            else:
                first_attacker, first_skill, first_defender = self.opponent_creature, opponent_skill, self.player_creature
                second_attacker, second_skill, second_defender = self.player_creature, player_skill, self.opponent_creature

        self._execute_skill(first_attacker, first_skill, first_defender)
        if first_defender.hp > 0:
            self._execute_skill(second_attacker, second_skill, second_defender)

    def _execute_skill(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
        else:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
        
        self._reset_creatures()
        
        # Add a button to return to the main menu
        return_button = Button("Return to Main Menu")
        choice = self._wait_for_choice(self.player, [return_button])
        
        # Transition back to the main menu
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
