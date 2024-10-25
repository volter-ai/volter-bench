from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random
import time


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self.check_battle_end():
                time.sleep(2)  # Give players time to read the result
                self._transition_to_scene("MainMenuScene")
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if second.hp > 0:
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        attacker_name = self.player.display_name if attacker == self.player_creature else self.opponent.display_name
        defender_name = self.opponent.display_name if attacker == self.player_creature else self.player.display_name
        
        message = f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!\n"
        message += f"It dealt {final_damage} damage to {defender_name}'s {defender.display_name}."
        self._show_text(self.player, message)
        self._show_text(self.opponent, message)

    def get_weakness_resistance_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost!")
            self._show_text(self.opponent, f"You defeated {self.player.display_name}'s {self.player_creature.display_name}. You won!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"You defeated {self.opponent.display_name}'s {self.opponent_creature.display_name}. You won!")
            self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} fainted. You lost!")
            return True
        return False
