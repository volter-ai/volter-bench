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

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choices = ["Attack", "Swap"]
        choice = random.choice(choices)
        
        if choice == "Attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("skill", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, new_creature))
            else:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("skill", self.opponent, skill))

    def determine_action_order(self):
        def get_speed(action):
            if action[0] == "swap":
                return float('inf')  # Swaps always go first
            return action[1].active_creature.speed

        # Sort by speed, with random order for equal speeds
        return sorted(self.turn_queue, key=lambda x: (get_speed(x), random.random()), reverse=True)

    def resolve_turn(self):
        ordered_actions = self.determine_action_order()
        
        for action, player, target in ordered_actions:
            if action == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "skill":
                self.resolve_skill(player, target)
        
        self.turn_queue.clear()

    def resolve_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature
        
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")
        
        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            self.end_battle(player)
            return

        if player == self.player:
            new_creature = self.choose_creature(player)
        else:
            new_creature = random.choice(available_creatures)
        
        if new_creature:
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        else:
            self.end_battle(player)

    def end_battle(self, losing_player):
        winner = self.player if losing_player == self.opponent else self.opponent
        self._show_text(self.player, f"{winner.display_name} won the battle!")
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self.end_battle(self.player)
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self.end_battle(self.opponent)
            return True
        return False

    def choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None
