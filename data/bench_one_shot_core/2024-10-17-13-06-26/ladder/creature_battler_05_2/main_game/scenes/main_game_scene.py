from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, BotListener
from main_game.models import Player, Creature, Skill
import random
from typing import Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        if self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name if self.player.active_creature else 'No active creature'} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} if self.player.active_creature else 'N/A')
{self.opponent.display_name}: {self.opponent.active_creature.display_name if self.opponent.active_creature else 'No active creature'} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} if self.opponent.active_creature else 'N/A')

> Attack
> Swap
> Back
"""

    def run(self):
        while True:
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            self.resolve_turn(player_action, opponent_action)
            if self.check_battle_end():
                break
        self.reset_creatures()

    def player_turn(self) -> Tuple[Player, SelectThing]:
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        return (self.player, self.get_player_action(self.player))

    def opponent_turn(self) -> Tuple[Player, SelectThing]:
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        return (self.opponent, self.get_player_action(self.opponent))

    def get_player_action(self, acting_player: Player) -> SelectThing:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button, back_button]
            choice = self._wait_for_choice(acting_player, choices)

            if attack_button == choice:
                attack_choice = self.get_attack_choice(acting_player)
                if attack_choice:
                    return attack_choice
            elif swap_button == choice:
                swap_choice = self.get_swap_choice(acting_player)
                if swap_choice:
                    return swap_choice
            elif back_button == choice:
                continue

    def get_attack_choice(self, acting_player: Player) -> SelectThing:
        if acting_player.active_creature:
            choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
            choices.append(Button("Back"))
            choice = self._wait_for_choice(acting_player, choices)
            if isinstance(choice, Button) and choice.display_name == "Back":
                return None
            return choice
        return None

    def get_swap_choice(self, acting_player: Player) -> SelectThing:
        available_creatures = [c for c in acting_player.creatures if c != acting_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, "No creatures available to swap.")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(acting_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def resolve_turn(self, player_action: Tuple[Player, SelectThing], opponent_action: Tuple[Player, SelectThing]):
        actions = [player_action, opponent_action]
        swaps = [action for action in actions if isinstance(action[1].thing, Creature)]
        attacks = [action for action in actions if isinstance(action[1].thing, Skill)]

        # Execute swaps first
        for acting_player, action in swaps:
            self.execute_swap(acting_player, action.thing)

        # Then execute attacks, ordered by speed
        attacks.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(attacks) == 2 and attacks[0][0].active_creature.speed == attacks[1][0].active_creature.speed:
            random.shuffle(attacks)

        for acting_player, action in attacks:
            defending_player = self.opponent if acting_player == self.player else self.player
            self.execute_attack(acting_player, defending_player, action.thing)
            if defending_player.active_creature.hp == 0:
                self.force_swap(defending_player)
            if self.check_battle_end():
                break

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        if attacker.active_creature and defender.active_creature:
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def execute_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
        if isinstance(player._listener, BotListener):
            new_creature = random.choice(available_creatures)
        else:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            new_creature = choice.thing
        self.execute_swap(player, new_creature)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, f"You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, f"You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = None
        self.opponent.active_creature = None
