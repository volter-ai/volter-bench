from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)
            
            if self.check_battle_end():
                break
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        self._show_text(self.player, f"{self.opponent.display_name} is choosing a skill...")
        return random.choice(self.opponent_creature.skills)

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
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
            self._show_text(self.player, f"Physical attack: {attacker.attack} + {skill.base_damage} - {defender.defense} = {raw_damage:.2f}")
        else:
            raw_damage = float(attacker.sp_attack * skill.base_damage / defender.sp_defense)
            self._show_text(self.player, f"Special attack: ({attacker.sp_attack} * {skill.base_damage}) / {defender.sp_defense} = {raw_damage:.2f}")

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        self._show_text(self.player, f"Weakness factor: {weakness_factor:.2f}")

        final_damage = int(weakness_factor * raw_damage)
        self._show_text(self.player, f"Final damage: {final_damage}")

        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name}'s HP reduced to {defender.hp}")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def check_battle_end(self):
        player_defeated = self.player_creature.hp == 0
        opponent_defeated = self.opponent_creature.hp == 0

        if player_defeated and opponent_defeated:
            self._show_text(self.player, "It's a draw! Both creatures were defeated simultaneously!")
            return True
        elif player_defeated:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif opponent_defeated:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
