from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> {self.player_creature.skills[0].display_name}
> {self.player_creature.skills[1].display_name}
"""

    def run(self):
        while True:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()

            first, second = self.determine_turn_order(player_skill, opponent_skill)
            self.execute_turn(first)
            if self.check_battle_end():
                break
            self.execute_turn(second)
            if self.check_battle_end():
                break

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill), (self.opponent, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill), (self.player, player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, player_skill), (self.opponent, opponent_skill)
            else:
                return (self.opponent, opponent_skill), (self.player, player_skill)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = self.calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
