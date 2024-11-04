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
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
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

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, foe_skill)
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, creature2, skill1), (self.opponent, creature2, creature1, skill2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, creature1, skill2), (self.player, creature1, creature2, skill1)
        else:
            if random.choice([True, False]):
                return (self.player, creature1, creature2, skill1), (self.opponent, creature2, creature1, skill2)
            else:
                return (self.opponent, creature2, creature1, skill2), (self.player, creature1, creature2, skill1)

    def execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = self.calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}! It dealt {damage} damage.")

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

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self.end_battle(False)
            return True
        elif self.opponent_creature.hp <= 0:
            self.end_battle(True)
            return True
        return False

    def end_battle(self, player_won):
        if player_won:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted. You won the battle!")
        else:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost the battle!")

        # Ask the player if they want to play again or quit
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [play_again_button, quit_button])

        if choice == play_again_button:
            # Reset creature HP and transition back to the main menu
            self.player_creature.hp = self.player_creature.max_hp
            self.opponent_creature.hp = self.opponent_creature.max_hp
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
