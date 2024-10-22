from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.player_creature = player.creatures[0]
        self.foe = app.create_bot("basic_opponent")
        self.foe_creature = self.foe.creatures[0]
        self.player_skill = None
        self.foe_skill = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.foe.display_name}'s {self.foe_creature.display_name} (HP: {self.foe_creature.hp}/{self.foe_creature.max_hp})

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            # Player Choice Phase
            self.player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures' HP after the battle
        self.reset_creatures()

        # Transition back to the MainMenuScene
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolution_phase(self):
        first, second = self.determine_order()
        self.execute_skill(*first)
        if second[1].hp > 0:
            self.execute_skill(*second)

    def determine_order(self):
        if self.player_creature.speed > self.foe_creature.speed:
            return (self.player, self.player_creature, self.player_skill, self.foe_creature), (self.foe, self.foe_creature, self.foe_skill, self.player_creature)
        elif self.player_creature.speed < self.foe_creature.speed:
            return (self.foe, self.foe_creature, self.foe_skill, self.player_creature), (self.player, self.player_creature, self.player_skill, self.foe_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_skill, self.foe_creature), (self.foe, self.foe_creature, self.foe_skill, self.player_creature)
            else:
                return (self.foe, self.foe_creature, self.foe_skill, self.player_creature), (self.player, self.player_creature, self.player_skill, self.foe_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
