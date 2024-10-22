from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []
        self.battle_ended = False

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
        self.setup_battle()
        self.battle_loop()

    def setup_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def battle_loop(self):
        while not self.battle_ended:
            self.player_turn()
            self.opponent_turn()
            self.resolve_turn()
            self.check_battle_end()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choice = self._wait_for_choice(self.opponent, [Button("Attack"), Button("Swap")])
        if choice.display_name == "Attack":
            skill = self.choose_skill(self.opponent)
            self.turn_queue.append(("attack", self.opponent, skill))
        else:
            new_creature = self.choose_creature(self.opponent)
            if new_creature:
                self.turn_queue.append(("swap", self.opponent, new_creature))
            else:
                # If no creatures to swap, default to attack
                skill = self.choose_skill(self.opponent)
                self.turn_queue.append(("attack", self.opponent, skill))

    def choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def choose_creature(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else (x[1].active_creature.speed, random.random())), reverse=True)
        
        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self.resolve_attack(player, target)

        self.turn_queue.clear()

    def resolve_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def force_swap(self, player):
        new_creature = self.choose_creature(player)
        if new_creature:
            player.active_creature = new_creature
            self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.battle_ended = True
            self.reset_creatures_state()
            self._quit_whole_game()
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self.battle_ended = True
            self.reset_creatures_state()
            self._quit_whole_game()

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
