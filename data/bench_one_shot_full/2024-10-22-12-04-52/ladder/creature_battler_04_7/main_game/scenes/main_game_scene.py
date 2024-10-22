from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> Use Skill
> Return to Main Menu
"""

    def run(self):
        while not self.battle_ended:
            self._show_text(self.player, str(self))
            
            # Player Choice Phase
            player_choice = self.player_choice_phase()
            
            if player_choice == "return_to_menu":
                self.battle_ended = True
                self._transition_to_scene("MainMenuScene")
                return

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_choice, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self.battle_ended = True
                self._show_text(self.player, "Battle ended. Returning to Main Menu.")
                self._transition_to_scene("MainMenuScene")
                return

        self.reset_creatures()

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        return_to_menu_button = Button("Return to Main Menu")
        choice = self._wait_for_choice(self.player, [use_skill_button, return_to_menu_button])
        
        if return_to_menu_button == choice:
            return "return_to_menu"
        
        if use_skill_button == choice:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            return skill_choice.thing

    def foe_choice_phase(self):
        return random.choice(self.opponent_creature.skills)

    def resolution_phase(self, player_skill, foe_skill):
        if player_skill == "return_to_menu":
            return

        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        
        if first == self.player_creature:
            self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent_creature, self.player_creature, foe_skill)
        else:
            self.execute_skill(self.opponent_creature, self.player_creature, foe_skill)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
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

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
