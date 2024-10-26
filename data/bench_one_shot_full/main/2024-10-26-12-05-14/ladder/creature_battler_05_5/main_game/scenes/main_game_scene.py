from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
import time


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                time.sleep(2)  # Give players time to read the battle result
                self.reset_creatures_state()
                self._transition_to_scene("MainMenuScene")
                break

    def player_choice_phase(self):
        if self.player.active_creature.hp > 0:
            self.get_player_action(self.player)

    def foe_choice_phase(self):
        if self.opponent.active_creature.hp > 0:
            self.get_player_action(self.opponent)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self.choose_skill(player)
                if skill:
                    self.turn_queue.append(("attack", player, skill))
                    break
            elif choice == swap_button:
                new_creature = self.choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append(("swap", player, new_creature))
                    break

    def choose_skill(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def choose_swap_creature(self, player):
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in player.creatures 
                   if creature != player.active_creature and creature.hp > 0] + [back_button]
        if len(choices) == 1:  # Only "Back" button
            return None
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed, random.random()), reverse=True)

        for action in self.turn_queue:
            if action[0] == "swap":
                player, new_creature = action[1], action[2]
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")
            elif action[0] == "attack":
                attacker, skill = action[1], action[2]
                defender = self.player if attacker == self.opponent else self.opponent
                self.execute_attack(attacker, defender, skill)

        self.turn_queue.clear()

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self.choose_swap_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
