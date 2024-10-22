from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.current_turn = "player"

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

{self.player.display_name}'s skills:
{self.get_skill_choices_str(self.player_creature)}

{self.foe.display_name}'s skills:
{self.get_skill_choices_str(self.foe_creature)}

Current turn: {self.current_turn.capitalize()}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            self.current_turn = "player"
            player_skill = self.player_choice_phase()
            self.current_turn = "foe"
            foe_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, foe_skill)
            
            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        self._show_text(self.player, f"{self.player.display_name}'s turn")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        self._show_text(self.player, f"{self.foe.display_name}'s turn")
        self._show_text(self.player, f"{self.foe.display_name}'s skills:\n{self.get_skill_choices_str(self.foe_creature)}")
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        chosen_skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)
        self._show_text(self.player, f"{self.foe.display_name} chose {chosen_skill.display_name}")
        return chosen_skill

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.foe_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if not self.check_battle_end():
            self.execute_skill(second, first, second_skill)

    def execute_skill(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {damage} damage.")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.foe_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
        else:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
        
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")

    def get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])
