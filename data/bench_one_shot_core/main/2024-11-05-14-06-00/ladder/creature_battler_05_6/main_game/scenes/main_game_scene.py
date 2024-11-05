from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


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
        self._initialize_battle()
        while True:
            self._player_turn(self.player)
            self._player_turn(self.opponent)
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        while True:
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return choice.thing

    def _choose_creature(self, player):
        while True:
            choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
            back_button = Button("Back")
            choices.append(back_button)
            if not choices:
                self._show_text(player, "No other creatures available to swap!")
                return None
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return choice.thing

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed))
        
        # Handle same speed scenario
        if len(self.turn_queue) == 2 and self.turn_queue[0][0].active_creature.speed == self.turn_queue[1][0].active_creature.speed:
            self.turn_queue = random.sample(self.turn_queue, len(self.turn_queue))

        for player, action, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self._resolve_attack(player, target)
            
            # Check for knocked out creatures after each action
            self._check_knocked_out(self.player)
            self._check_knocked_out(self.opponent)

        self.turn_queue.clear()

    def _resolve_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_knocked_out(self, player):
        if player.active_creature.hp == 0:
            self._show_text(player, f"{player.active_creature.display_name} has been knocked out!")
            new_creature = self._force_swap(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
            else:
                self._show_text(player, f"{player.display_name} has no more creatures left!")

    def _force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return None
        if len(available_creatures) == 1:
            return available_creatures[0]
        choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, "Choose a creature to swap in:")
        return self._wait_for_choice(player, choices).thing

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
