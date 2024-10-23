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
        self._show_text(self.player, "Battle start!")
        while True:
            self.player_turn()
            if self.check_battle_end():
                break
            self.opponent_turn()
            if self.check_battle_end():
                break
            self.resolve_turn()

        # Reset creatures' HP
        self.reset_creatures_hp()

        # Transition back to MainMenuScene
        self._show_text(self.player, "Returning to Main Menu...")
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    self.turn_queue.append(("player", "attack", skill_choice.thing))
                    break
            elif choice == swap_button:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature.hp > 0 and creature != self.player.active_creature]
                creature_choice = self._wait_for_choice(self.player, creature_choices + [Button("Back")])
                if isinstance(creature_choice, SelectThing):
                    self.turn_queue.append(("player", "swap", creature_choice.thing))
                    break

    def opponent_turn(self):
        choices = [Button("Attack"), Button("Swap")]
        choice = self._wait_for_choice(self.opponent, choices)

        if choice.display_name == "Attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("opponent", "attack", skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append(("opponent", "swap", creature))

    def resolve_turn(self):
        def get_speed(turn):
            player, action, target = turn
            if action == "swap":
                return float('inf')  # Swapping always goes first
            else:
                return self.player.active_creature.speed if player == "player" else self.opponent.active_creature.speed

        self.turn_queue.sort(key=lambda x: (-get_speed(x), x[0]))  # Sort by speed (descending) and then by player

        for turn in self.turn_queue:
            player, action, target = turn
            if action == "swap":
                self.swap_creature(player, target)
            elif action == "attack":
                self.execute_attack(player, target)

        self.turn_queue.clear()

    def swap_creature(self, player, creature):
        if player == "player":
            self.player.active_creature = creature
            self._show_text(self.player, f"{self.player.display_name} swapped to {creature.display_name}!")
        else:
            self.opponent.active_creature = creature
            self._show_text(self.player, f"{self.opponent.display_name} swapped to {creature.display_name}!")

    def execute_attack(self, attacker, skill):
        if attacker == "player":
            attacker_creature = self.player.active_creature
            defender_creature = self.opponent.active_creature
        else:
            attacker_creature = self.opponent.active_creature
            defender_creature = self.player.active_creature

        damage = self.calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender_creature.display_name} fainted!")
            self.force_swap(attacker)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)

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
        if player == "player":
            available_creatures = [c for c in self.player.creatures if c.hp > 0]
            if available_creatures:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                choice = self._wait_for_choice(self.player, creature_choices)
                self.player.active_creature = choice.thing
                self._show_text(self.player, f"{self.player.display_name} sent out {choice.thing.display_name}!")
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.opponent.active_creature = creature
                self._show_text(self.player, f"{self.opponent.display_name} sent out {creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def reset_creatures_hp(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
