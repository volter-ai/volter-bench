import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.active_creature
        foe_creature = self.foe.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.foe.display_name}'s {foe_creature.display_name}: HP {foe_creature.hp}/{foe_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]

    def game_loop(self):
        while True:
            turn_queue = []
            turn_queue.extend(self._player_choice_phase(self.player))
            turn_queue.extend(self._player_choice_phase(self.foe))
            self._resolution_phase(turn_queue)

            if self._check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self._choose_skill(player)
                if skill:
                    return [(player, "attack", skill)]
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    return [(player, "swap", new_creature)]

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self, turn_queue):
        # Sort the turn queue, considering speed and adding a random tiebreaker
        turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))

        # Handle swaps first
        for player, action_type, action in turn_queue:
            if action_type == "swap":
                self._perform_swap(player, action)

        # Then handle attacks
        for player, action_type, action in turn_queue:
            if action_type == "attack":
                self._perform_attack(player, action)

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.foe if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)  # Explicitly convert to integer
        return max(1, final_damage)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.foe.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        elif self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        elif self.foe.active_creature.hp == 0:
            self._force_swap(self.foe)
        return False

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            self._perform_swap(player, choice.thing)
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
