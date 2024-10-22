import random
from typing import List, Union

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.action_queue: List[Union[SelectThing, None]] = []
        self.swapped_players: List[Player] = []
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

    def battle_loop(self):
        while True:
            self.action_queue.clear()
            self.swapped_players.clear()
            self.player_turn()
            self.bot_turn()
            self.resolve_turn()

            battle_result = self.check_battle_end()
            if battle_result != "ongoing":
                self.end_battle(battle_result)
                break

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                attack_action = self.choose_attack(self.player)
                if attack_action:
                    self.action_queue.append(attack_action)
                    return
            elif swap_button == choice:
                swap_action = self.choose_swap(self.player)
                if swap_action:
                    self.action_queue.append(swap_action)
                    return

    def bot_turn(self):
        while True:
            choice = random.choice(["Attack", "Swap"])
            if choice == "Attack":
                attack_action = self.choose_attack(self.bot)
                if attack_action:
                    self.action_queue.append(attack_action)
                    return
            else:
                swap_action = self.choose_swap(self.bot)
                if swap_action:
                    self.action_queue.append(swap_action)
                    return

    def choose_attack(self, actor: Player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in actor.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return choice

    def choose_swap(self, actor: Player):
        available_creatures = [c for c in actor.creatures if c != actor.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(actor, "No creatures available to swap!")
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return choice

    def resolve_turn(self):
        # Execute swap actions first
        for action in self.action_queue:
            actor = self.get_actor(action)
            if isinstance(action.thing, Creature):
                self.swap_creature(actor, action.thing)
                self.swapped_players.append(actor)

        # Sort and execute attack actions
        attack_actions = [action for action in self.action_queue if isinstance(action.thing, Skill)]
        attack_actions.sort(key=lambda x: (self.get_actor(x).active_creature.speed, random.random()), reverse=True)
        
        for action in attack_actions:
            actor = self.get_actor(action)
            self.execute_skill(actor, action.thing)

    def get_actor(self, action):
        return self.player if action in [SelectThing(c) for c in self.player.creatures] + [SelectThing(s) for s in self.player.active_creature.skills] else self.bot

    def swap_creature(self, actor: Player, new_creature: Creature):
        actor.active_creature = new_creature
        self._show_text(actor, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def execute_skill(self, actor: Player, skill: Skill):
        target = self.bot if actor == self.player else self.player
        # Check if the target has swapped creatures
        if target in self.swapped_players:
            self._show_text(actor, f"{actor.active_creature.display_name} attacks the swapped-in {target.active_creature.display_name}!")
        damage = self.calculate_damage(actor.active_creature, target.active_creature, skill)
        target.active_creature.hp = max(0, target.active_creature.hp - damage)
        self._show_text(actor, f"{actor.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            return "loss"
        elif all(c.hp == 0 for c in self.bot.creatures):
            return "win"

        if self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        if self.bot.active_creature.hp == 0:
            self.force_swap(self.bot)

        return "ongoing"

    def force_swap(self, actor: Player):
        available_creatures = [c for c in actor.creatures if c.hp > 0]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            self.swap_creature(actor, new_creature)
        else:
            self._show_text(actor, f"{actor.display_name} has no more creatures able to battle!")

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def end_battle(self, result: str):
        if result == "win":
            self._show_text(self.player, "Congratulations! You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle. Better luck next time!")
        
        self.on_exit()

    def on_exit(self):
        self.reset_creatures()
        self._quit_whole_game()
