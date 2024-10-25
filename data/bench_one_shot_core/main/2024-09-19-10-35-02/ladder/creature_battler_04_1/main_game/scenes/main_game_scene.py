from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices()}
"""

    def get_skill_choices(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self.show_battle_result()
                self._transition_to_scene("MainMenuScene")
                return

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        foe_skills = self.foe_creature.skills
        skill_names = ", ".join([skill.display_name for skill in foe_skills])
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} can use: {skill_names}")
        chosen_skill = random.choice(foe_skills)
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} chose {chosen_skill.display_name}!")
        return chosen_skill

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.foe_creature)
        
        if first == self.player_creature:
            self.execute_skill(self.player_creature, self.foe_creature, player_skill)
            if self.foe_creature.hp > 0:
                self.execute_skill(self.foe_creature, self.player_creature, foe_skill)
        else:
            self.execute_skill(self.foe_creature, self.player_creature, foe_skill)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, self.foe_creature, player_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.choice([(creature1, creature2), (creature2, creature1)])

    def execute_skill(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)
        
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(max(1, type_factor * raw_damage))  # Ensure at least 1 damage is dealt
        return final_damage

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.foe_creature.hp <= 0

    def show_battle_result(self):
        if self.player_creature.hp <= 0:
            result = f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!"
        else:
            result = f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!"
        
        self._show_text(self.player, result)
        self._wait_for_choice(self.player, [Button("Continue")])
