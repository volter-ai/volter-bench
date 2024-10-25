from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Transition back to the main menu after the battle ends
        self.return_to_main_menu()

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        # Simplified bot decision-making: randomly choose a skill
        return random.choice(self.opponent_creature.skills)

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, foe_skill)
        
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, skill1, self.opponent, creature2), (self.opponent, creature2, skill2, self.player, creature1)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, skill2, self.player, creature1), (self.player, creature1, skill1, self.opponent, creature2)
        else:
            if random.choice([True, False]):
                return (self.player, creature1, skill1, self.opponent, creature2), (self.opponent, creature2, skill2, self.player, creature1)
            else:
                return (self.opponent, creature2, skill2, self.player, creature1), (self.player, creature1, skill1, self.opponent, creature2)

    def execute_skill(self, attacker, attacker_creature, skill, defender, defender_creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack * skill.base_damage) // defender_creature.sp_defense

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = (weakness_factor * raw_damage) // 1  # Integer division to ensure integer result

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        effectiveness = {
            "fire": {"fire": 1, "water": 1, "leaf": 2},
            "water": {"fire": 2, "water": 1, "leaf": 1},
            "leaf": {"fire": 1, "water": 2, "leaf": 1}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp

    def return_to_main_menu(self):
        self._show_text(self.player, "Resetting your creatures' state and returning to the main menu...")
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")
