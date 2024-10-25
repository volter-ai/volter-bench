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
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            opponent_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                return  # Exit the run method after transitioning

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def determine_execution_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
        elif self.player_creature.speed < self.opponent_creature.speed:
            return [(self.opponent.prototype_id, self.opponent_creature), (self.player.prototype_id, self.player_creature)]
        else:
            # Equal speed, randomly decide
            order = [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
            random.shuffle(order)
            return order

    def resolution_phase(self, player_skill, opponent_skill):
        execution_order = self.determine_execution_order()
        skills = {self.player.prototype_id: player_skill, self.opponent.prototype_id: opponent_skill}

        for attacker_id, attacker_creature in execution_order:
            defender_id, defender_creature = next((p_id, c) for p_id, c in execution_order if p_id != attacker_id)
            self.execute_skill(attacker_id, attacker_creature, skills[attacker_id], defender_creature)
            if defender_creature.hp <= 0:
                break  # Stop if the defender is defeated

    def execute_skill(self, attacker_id, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        attacker = self.player if attacker_id == self.player.prototype_id else self.opponent
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and defender_type == "leaf":
            return 2
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "fire":
            return 2
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "water":
            return 2
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
