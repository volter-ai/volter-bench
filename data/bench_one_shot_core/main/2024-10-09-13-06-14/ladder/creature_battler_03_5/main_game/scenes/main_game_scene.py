from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")

        battle_ongoing = True
        while battle_ongoing:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            opponent_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)

            battle_ongoing = not self.check_battle_end()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature), (self.opponent, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature), (self.player, self.player_creature)
        else:
            first = random.choice([(self.player, self.player_creature), (self.opponent, self.opponent_creature)])
            second = (self.opponent, self.opponent_creature) if first[0] == self.player else (self.player, self.player_creature)
            return first, second

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order()
        first_skill = player_skill if first[0] == self.player else opponent_skill
        second_skill = opponent_skill if first[0] == self.player else player_skill

        self.execute_skill(first[0], first[1], first_skill, second[1])
        if second[1].hp > 0:
            self.execute_skill(second[0], second[1], second_skill, first[1])

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = float(attacker_creature.attack) + float(skill.base_damage) - float(defender_creature.defense)
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {final_damage} damage!")
        self._show_text(self.opponent, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
