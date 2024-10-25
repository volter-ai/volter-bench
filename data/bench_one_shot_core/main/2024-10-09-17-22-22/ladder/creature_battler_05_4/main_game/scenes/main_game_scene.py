from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
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
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.opponent)
            self._resolution_phase()
            
            if self._check_battle_end():
                break

    def _player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self._choose_skill(current_player)
                if skill:
                    self.turn_queue.append((current_player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(current_player)
                if new_creature:
                    self.turn_queue.append((current_player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self):
        # Sort the turn queue, handling equal speed scenarios
        self.turn_queue.sort(key=lambda x: (
            x[1] != "swap",  # Swaps always go first
            -x[0].active_creature.speed,  # Higher speed goes first
            random.random()  # Random factor for equal speeds
        ))
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                self._execute_skill(player, action)

        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack) + float(skill.base_damage) - float(defender_creature.defense)
        else:
            raw_damage = (float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense)) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5,
            ("normal", "fire"): 1,
            ("normal", "water"): 1,
            ("normal", "leaf"): 1
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self._transition_to_scene("MainMenuScene")
                return True

        if self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        if self.opponent.active_creature.hp == 0:
            self._force_swap(self.opponent)

        return False

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} swapped to {player.active_creature.display_name}!")
