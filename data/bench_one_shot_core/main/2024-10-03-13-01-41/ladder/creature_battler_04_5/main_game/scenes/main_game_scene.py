from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.player_creature = player.creatures[0]
        self.foe = app.create_bot("basic_opponent")
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.foe.display_name}'s {self.foe_creature.display_name} (HP: {self.foe_creature.hp}/{self.foe_creature.max_hp})

Player's turn:
> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            if player_skill is None:
                return

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            if self.check_battle_end():
                return

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

        if choice == quit_button:
            self.reset_creatures_state()
            self._quit_whole_game()
            return None

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        return skill_choice.thing

    def foe_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        skill_choice = self._wait_for_choice(self.foe, skill_choices)
        return skill_choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.foe_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if not self.check_battle_end():
            self.execute_skill(second, first, second_skill)

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
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

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
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 0.5, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} has been defeated!")
            self._show_text(self.player, f"You lost the battle against {self.foe.display_name}'s {self.foe_creature.display_name}!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.foe_creature.display_name} has been defeated!")
            self._show_text(self.player, f"You won the battle with your {self.player_creature.display_name}!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
