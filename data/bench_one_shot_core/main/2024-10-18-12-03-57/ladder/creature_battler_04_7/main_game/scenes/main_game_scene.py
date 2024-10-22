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
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")
        player_won = self.battle_loop()
        self.show_battle_result(player_won)
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            if self.battle_turn():
                return self.player_creature.hp > 0

    def battle_turn(self):
        player_skill = self.player_choice_phase()
        opponent_skill = self.foe_choice_phase()
        return self.resolution_phase(player_skill, opponent_skill)

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        battle_end = self.execute_skill(first, second, first_skill)
        if not battle_end:
            battle_end = self.execute_skill(second, first, second_skill)

        return battle_end

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

        attacker_player = self.player if attacker == self.player_creature else self.opponent
        defender_player = self.opponent if attacker == self.player_creature else self.player

        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} takes {damage} damage!")

        if defender.hp == 0:
            self._show_text(self.player, f"{defender.display_name} is knocked out!")
            self._show_text(self.player, f"{attacker_player.display_name} wins the battle!")
            return True
        return False

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def show_battle_result(self, player_won):
        result_message = "Congratulations! You won the battle!" if player_won else "You lost the battle. Better luck next time!"
        self._show_text(self.player, result_message)
        
        continue_button = Button("Return to Main Menu")
        self._wait_for_choice(self.player, [continue_button])
