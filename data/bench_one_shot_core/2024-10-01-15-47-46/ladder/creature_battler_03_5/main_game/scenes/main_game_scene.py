from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_count = 0
        self.max_battles = 3  # Limit the number of battles

    def __str__(self):
        return f"""
Player: {self.player.display_name}
Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})

Opponent: {self.opponent.display_name}
Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
        """

    def run(self):
        while self.battle_count < self.max_battles:
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()

            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                self._show_battle_result()
                self.battle_count += 1
                self._reset_battle()
                
                if self.battle_count < self.max_battles:
                    choice = self._wait_for_choice(self.player, [
                        Button("Continue"),
                        Button("Quit to Main Menu")
                    ])
                    if choice.display_name == "Quit to Main Menu":
                        break
                else:
                    self._show_text(self.player, "You've reached the maximum number of battles.")
                    self._show_text(self.opponent, "You've reached the maximum number of battles.")

        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self._execute_skill(first, second, first_skill)
        if second.hp > 0:
            self._execute_skill(second, first, second_skill)

    def _determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def _execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} on {defender.display_name} for {final_damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} on {defender.display_name} for {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _show_battle_result(self):
        if self.player_creature.hp <= 0:
            result = "You lost the battle!"
        else:
            result = "You won the battle!"
        self._show_text(self.player, result)
        self._show_text(self.opponent, "The battle has ended.")

    def _reset_battle(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
