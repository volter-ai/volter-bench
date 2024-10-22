from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.reset_creatures()

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name}: HP {self.player.active_creature.hp}/{self.player.active_creature.max_hp}
{self.opponent.display_name}'s {self.opponent.active_creature.display_name}: HP {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")
        while True:
            self.turn_counter += 1
            player_action = self.player_choice_phase(self.player)
            opponent_action = self.player_choice_phase(self.opponent)
            self.resolution_phase(player_action, opponent_action)
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue
                return ("attack", skill_choice.thing)
            elif swap_button == choice:
                creature_choices = [SelectThing(creature) for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
                back_button = Button("Back")
                creature_choices.append(back_button)
                if creature_choices:
                    creature_choice = self._wait_for_choice(current_player, creature_choices)
                    if creature_choice == back_button:
                        continue
                    return ("swap", creature_choice.thing)
                else:
                    self._show_text(current_player, "No other creatures available to swap!")

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for current_player, action in actions:
            if action[0] == "swap":
                self.perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self.perform_attack(current_player, action[1])

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)  # Explicitly convert to integer
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            self.perform_swap(player, new_creature)
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures left!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"{self.opponent.display_name} wins the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"{self.player.display_name} wins the battle!")
            return True
        return False
