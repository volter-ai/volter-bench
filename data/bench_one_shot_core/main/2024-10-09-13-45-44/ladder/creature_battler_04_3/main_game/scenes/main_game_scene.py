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

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.opponent_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_choice_phase(self):
        return random.choice(self.opponent_creature.skills)

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

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
        damage, raw_damage, type_factor = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Raw damage: {raw_damage:.2f}, Type factor: {type_factor:.2f}")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float((attacker.sp_attack / defender.sp_defense) * skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return final_damage, raw_damage, type_factor

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5,
            ("normal", "normal"): 1.0,
            ("normal", "fire"): 1.0,
            ("normal", "water"): 1.0,
            ("normal", "leaf"): 1.0,
            ("fire", "normal"): 1.0,
            ("water", "normal"): 1.0,
            ("leaf", "normal"): 1.0
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def check_battle_end(self):
        return self.player_creature.hp == 0 or self.opponent_creature.hp == 0

    def end_battle(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

        self.reset_creatures()
        self.reset_opponent_creatures()
        
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp

    def reset_opponent_creatures(self):
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
