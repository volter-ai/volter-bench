from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name if self.player.active_creature else 'No creature'}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp if self.player.active_creature else 0}

{self.opponent.display_name}'s {self.opponent.active_creature.display_name if self.opponent.active_creature else 'No creature'}
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp if self.opponent.active_creature else 0}

> Attack
> Swap
"""

    def run(self):
        while True:
            self.turn_counter += 1
            player_action = self.player_turn(self.player)
            opponent_action = self.player_turn(self.opponent)
            self.resolve_turn(player_action, opponent_action)

            if self.check_battle_end():
                break

        self.reset_creatures_state()

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                action = self.choose_attack(current_player)
            elif swap_button == choice:
                action = self.choose_swap(current_player)

            if action is not None:
                return action

    def choose_attack(self, current_player):
        if not current_player.active_creature:
            self._show_text(current_player, f"{current_player.display_name} has no active creature to attack with!")
            return None
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        skill_choices.append(back_button)
        skill_choice = self._wait_for_choice(current_player, skill_choices)
        if skill_choice == back_button:
            return None
        return ("attack", skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, f"{current_player.display_name} has no creatures available to swap!")
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        creature_choice = self._wait_for_choice(current_player, creature_choices)
        if creature_choice == back_button:
            return None
        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        actions = [(player, action) for player, action in actions if action is not None]
        
        # Random tie-breaking for skill execution order
        random.shuffle(actions)
        actions.sort(key=lambda x: x[0].active_creature.speed if x[0].active_creature else 0, reverse=True)

        for current_player, action in actions:
            if action[0] == "swap":
                self.perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self.perform_attack(current_player, action[1])

            if self.check_knockout(current_player):
                break

    def perform_swap(self, current_player, new_creature):
        current_player.active_creature = new_creature
        self._show_text(current_player, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        if not defender.active_creature:
            self._show_text(attacker, f"{defender.display_name} has no active creature to attack!")
            return
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_knockout(self, current_player):
        if current_player.active_creature.hp == 0:
            self._show_text(current_player, f"{current_player.active_creature.display_name} was knocked out!")
            available_creatures = [creature for creature in current_player.creatures if creature.hp > 0]
            if available_creatures:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choice = self._wait_for_choice(current_player, creature_choices)
                self.perform_swap(current_player, creature_choice.thing)
                return False
            else:
                return True
        return False

    def check_battle_end(self):
        for current_player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in current_player.creatures):
                winner = self.opponent if current_player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
