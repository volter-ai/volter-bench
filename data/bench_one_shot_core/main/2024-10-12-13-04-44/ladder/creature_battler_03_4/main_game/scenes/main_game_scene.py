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
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0:
                self.end_battle()
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
        self.execute_skill(*first)
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self.execute_skill(*second)

    def determine_order(self, player_creature, opponent_creature, player_skill, opponent_skill):
        if player_creature.speed > opponent_creature.speed:
            return (self.player, player_creature, player_skill, self.opponent, opponent_creature), (self.opponent, opponent_creature, opponent_skill, self.player, player_creature)
        elif player_creature.speed < opponent_creature.speed:
            return (self.opponent, opponent_creature, opponent_skill, self.player, player_creature), (self.player, player_creature, player_skill, self.opponent, opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, player_creature, player_skill, self.opponent, opponent_creature), (self.opponent, opponent_creature, opponent_skill, self.player, player_creature)
            else:
                return (self.opponent, opponent_creature, opponent_skill, self.player, player_creature), (self.player, player_creature, player_skill, self.opponent, opponent_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}'s {defender_creature.display_name}!")

    def calculate_weakness_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._transition_to_scene("MainMenuScene")
