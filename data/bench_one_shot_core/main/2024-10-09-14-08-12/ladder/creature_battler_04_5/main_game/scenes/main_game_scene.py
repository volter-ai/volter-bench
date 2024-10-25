from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_count = 0

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            self.turn_count += 1
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if second.hp > 0:
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return tuple(random.sample([creature1, creature2], 2))

    def execute_skill(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        weakness_factor = self.get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        return final_damage

    def get_weakness_factor(self, skill_type, defender_type):
        weakness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return weakness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.turn_count >= 100:
            return True
        return self.player_creature.hp == 0 or self.opponent_creature.hp == 0

    def end_battle(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
        else:
            self._show_text(self.player, "The battle ended in a tie!")
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
