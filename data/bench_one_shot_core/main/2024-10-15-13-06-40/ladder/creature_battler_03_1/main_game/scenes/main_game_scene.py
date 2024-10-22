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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
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

    def resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed == self.opponent_creature.speed:
            # Randomly choose which creature goes first when speeds are equal
            first_attacker, first_skill, second_attacker, second_skill = random.choice([
                (self.player, player_skill, self.opponent, foe_skill),
                (self.opponent, foe_skill, self.player, player_skill)
            ])
            self._show_text(self.player, f"{first_attacker.display_name}'s creature attacks first!")
            self.execute_skill(first_attacker, first_attacker.creatures[0], first_skill, second_attacker.creatures[0])
            if second_attacker.creatures[0].hp > 0:
                self.execute_skill(second_attacker, second_attacker.creatures[0], second_skill, first_attacker.creatures[0])
        elif self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
        else:
            self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.get_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def get_weakness_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and creature_type == "leaf":
            return 2
        elif skill_type == "fire" and creature_type == "water":
            return 0.5
        elif skill_type == "water" and creature_type == "fire":
            return 2
        elif skill_type == "water" and creature_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and creature_type == "water":
            return 2
        elif skill_type == "leaf" and creature_type == "fire":
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            result = "You lost the battle!"
        else:
            result = "You won the battle!"
        self._show_text(self.player, result)
        
        continue_button = Button("Continue")
        self._wait_for_choice(self.player, [continue_button])
        
        self._transition_to_scene("MainMenuScene")
