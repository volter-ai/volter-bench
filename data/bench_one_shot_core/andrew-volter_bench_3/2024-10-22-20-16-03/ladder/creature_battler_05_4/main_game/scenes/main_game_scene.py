from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player_action = None
        self.opponent_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.opponent)  # Bot uses the same choice phase
            self._resolution_phase()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, current_player):
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
                if current_player == self.player:
                    self.player_action = ("attack", skill_choice.thing)
                else:
                    self.opponent_action = ("attack", skill_choice.thing)
                break
            elif swap_button == choice:
                creature_choices = [SelectThing(creature) for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
                back_button = Button("Back")
                creature_choices.append(back_button)
                if creature_choices:
                    creature_choice = self._wait_for_choice(current_player, creature_choices)
                    if creature_choice == back_button:
                        continue
                    if current_player == self.player:
                        self.player_action = ("swap", creature_choice.thing)
                    else:
                        self.opponent_action = ("swap", creature_choice.thing)
                    break
                else:
                    self._show_text(current_player, "No other creatures available to swap!")

    def _resolution_phase(self):
        # Execute swap actions first
        if self.player_action[0] == "swap":
            self._execute_swap(self.player, self.player_action[1])
        if self.opponent_action[0] == "swap":
            self._execute_swap(self.opponent, self.opponent_action[1])

        # Then execute attack actions
        if self.player_action[0] == "attack" and self.opponent_action[0] == "attack":
            first_player, second_player = self._determine_turn_order()
            self._execute_attack(first_player, self.opponent if first_player == self.player else self.player, 
                                 self.player_action[1] if first_player == self.player else self.opponent_action[1])
            if not self._check_battle_end():
                self._execute_attack(second_player, self.opponent if second_player == self.player else self.player, 
                                     self.opponent_action[1] if second_player == self.opponent else self.player_action[1])
        elif self.player_action[0] == "attack":
            self._execute_attack(self.player, self.opponent, self.player_action[1])
        elif self.opponent_action[0] == "attack":
            self._execute_attack(self.opponent, self.player, self.opponent_action[1])

    def _determine_turn_order(self):
        player_speed = self.player.active_creature.speed
        opponent_speed = self.opponent.active_creature.speed
        
        if player_speed > opponent_speed:
            return self.player, self.opponent
        elif opponent_speed > player_speed:
            return self.opponent, self.player
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def _execute_attack(self, attacker, defender, skill):
        attacking_creature = attacker.active_creature
        defending_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = float(attacking_creature.attack + skill.base_damage - defending_creature.defense)
        else:
            raw_damage = float(attacking_creature.sp_attack) / float(defending_creature.sp_defense) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defending_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defending_creature.hp = max(0, defending_creature.hp - final_damage)
        self._show_text(attacker, f"{attacking_creature.display_name} used {skill.display_name} and dealt {final_damage} damage!")

        if defending_creature.hp == 0:
            self._show_text(defender, f"{defending_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _execute_swap(self, player, new_creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(player, f"{old_creature.display_name} was swapped out for {new_creature.display_name}!")

    def _calculate_weakness_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        if skill_type == "normal":
            return 1.0
        return effectiveness.get((skill_type, creature_type), 1.0)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = creature_choice.thing
            self._show_text(player, f"{player.active_creature.display_name} was sent out!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        self._transition_to_scene("MainMenuScene")
