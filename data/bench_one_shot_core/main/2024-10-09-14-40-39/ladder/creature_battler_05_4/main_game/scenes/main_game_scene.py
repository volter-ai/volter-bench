from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_queue = []
        self.battle_ended = False

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
{self.opponent.display_name}: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while not self.battle_ended:
            self._player_turn()
            if self._check_battle_end():
                break
            self._opponent_turn()
            if self._check_battle_end():
                break
            self._resolve_turn()
        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self):
        while True:
            if self.player.active_creature.hp <= 0:
                if not self._force_swap(self.player):
                    break

            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif choice == swap_button:
                if self._attempt_swap(self.player):
                    break

    def _opponent_turn(self):
        if self.opponent.active_creature.hp <= 0:
            if not self._force_swap(self.opponent):
                return

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.opponent, choices)

        if choice == attack_button:
            skill = self._choose_skill(self.opponent)
            if skill:
                self.turn_queue.append(("skill", self.opponent, skill))
        elif choice == swap_button:
            self._attempt_swap(self.opponent)

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: self._get_action_priority(x), reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "skill":
                self._execute_skill(player, target)
            
            if self._check_battle_end():
                break

        self.turn_queue.clear()

    def _get_action_priority(self, action_tuple):
        action, player, target = action_tuple
        if action == "swap":
            return float('inf')  # Swaps always go first
        else:  # action == "skill"
            speed = player.active_creature.speed
            return speed + random.random()  # Add small random value as tie-breaker

    def _execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack + skill.base_damage - defender_creature.defense)
        else:
            raw_damage = float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense) * float(skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender_creature.display_name} was knocked out!")

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        # Normal type is neither effective nor ineffective against any other types,
        # so it always returns 1.0 (default value) when not found in the effectiveness dictionary
        return effectiveness.get((skill_type, defender_type), 1.0)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = self._choose_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
                return True
        self._show_text(player, f"{player.display_name} has no more creatures available!")
        return False

    def _attempt_swap(self, player):
        new_creature = self._choose_creature(player)
        if new_creature:
            self.turn_queue.append(("swap", player, new_creature))
            return True
        else:
            self._show_text(player, f"{player.display_name} has no other creatures to swap to!")
            return False

    def _choose_skill(self, player):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type}, {'Physical' if skill.is_physical else 'Special'})") for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            return None
        choices = [SelectThing(creature, label=f"{creature.display_name} (HP: {creature.hp}/{creature.max_hp})") for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _check_battle_end(self):
        player_creatures_alive = any(creature.hp > 0 for creature in self.player.creatures)
        opponent_creatures_alive = any(creature.hp > 0 for creature in self.opponent.creatures)

        if not player_creatures_alive and not opponent_creatures_alive:
            self._show_text(self.player, "The battle ended in a tie!")
            self.battle_ended = True
            return True
        elif not player_creatures_alive:
            self._show_text(self.player, "You lost the battle!")
            self.battle_ended = True
            return True
        elif not opponent_creatures_alive:
            self._show_text(self.player, "You won the battle!")
            self.battle_ended = True
            return True
        return False

    def _reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = None
        self.opponent.active_creature = None
