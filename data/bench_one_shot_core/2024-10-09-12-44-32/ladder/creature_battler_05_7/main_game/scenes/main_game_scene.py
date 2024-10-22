import random
from typing import Optional, Tuple

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        self.battle_loop()
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            player_action = self.player_turn()
            bot_action = self.bot_turn()
            self.resolve_turn(player_action, bot_action)

            if self.check_battle_end():
                break

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                attack_result = self.choose_attack(self.player)
                if attack_result:
                    return attack_result
            elif swap_button == choice:
                swap_result = self.choose_swap(self.player)
                if swap_result:
                    return swap_result

    def bot_turn(self):
        choices = ["Attack", "Swap"]
        choice = random.choice(choices)

        if choice == "Attack":
            return self.choose_attack(self.bot)
        else:
            swap_result = self.choose_swap(self.bot)
            if swap_result:
                return swap_result
            else:
                # If swap is not possible, default to attack
                return self.choose_attack(self.bot)

    def choose_attack(self, actor: Player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in actor.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return ("Attack", choice.thing)

    def choose_swap(self, actor: Player) -> Optional[Tuple[str, Creature]]:
        available_creatures = [c for c in actor.creatures if c != actor.active_creature and c.hp > 0]
        if not available_creatures:
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return ("Swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [
            (self.player, player_action),
            (self.bot, bot_action)
        ]

        # Resolve swaps first
        for actor, action in actions:
            if action and action[0] == "Swap":
                self.perform_swap(actor, action[1])

        # Resolve attacks
        actions = sorted(actions, key=lambda x: x[0].active_creature.speed if x[1] else 0, reverse=True)
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)  # Randomize order if speeds are equal
        for actor, action in actions:
            if action and action[0] == "Attack":
                self.perform_attack(actor, action[1])
            self.check_and_force_swap(actor)

    def perform_swap(self, actor: Player, new_creature: Creature):
        actor.active_creature = new_creature
        self._show_text(actor, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker: Player, skill: Skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = float(self.get_type_factor(skill.skill_type, defender.creature_type))
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_and_force_swap(self, actor: Player):
        if actor.active_creature.hp == 0:
            available_creatures = [c for c in actor.creatures if c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.perform_swap(actor, new_creature)
            else:
                self._show_text(actor, f"{actor.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
