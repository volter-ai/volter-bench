from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Skill
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
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

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
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice == back_button:
                    continue
                self.turn_queue.append(("attack", self.player, skill_choice.thing))
                break
            elif choice == swap_button:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                if creature_choices:
                    back_button = Button("Back")
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    if creature_choice == back_button:
                        continue
                    self.turn_queue.append(("swap", self.player, creature_choice.thing))
                    break
                else:
                    self._show_text(self.player, "No other creatures available to swap!")

    def opponent_turn(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(self.opponent, [attack_button, swap_button])

        if choice == attack_button:
            skill_choice = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill_choice))
        elif choice == swap_button:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                creature_choice = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, creature_choice))
            else:
                skill_choice = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill_choice))

    def resolve_turn(self):
        # Sort the turn queue based on action type and speed
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)

        # Resolve ties randomly
        i = 0
        while i < len(self.turn_queue) - 1:
            if (self.turn_queue[i][0] != "swap" and self.turn_queue[i+1][0] != "swap" and
                self.turn_queue[i][1].active_creature.speed == self.turn_queue[i+1][1].active_creature.speed):
                if random.choice([True, False]):
                    self.turn_queue[i], self.turn_queue[i+1] = self.turn_queue[i+1], self.turn_queue[i]
            i += 1

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                attacker = player
                defender = self.opponent if player == self.player else self.player
                self.resolve_attack(attacker, defender, target)

        self.turn_queue.clear()

    def resolve_attack(self, attacker: Player, defender: Player, skill: Skill):
        attack_creature = attacker.active_creature
        defend_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attack_creature.attack + skill.base_damage - defend_creature.defense
        else:
            raw_damage = (attack_creature.sp_attack / defend_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defend_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defend_creature.hp = max(0, defend_creature.hp - final_damage)

        self._show_text(self.player, f"{attack_creature.display_name} used {skill.display_name} on {defend_creature.display_name} for {final_damage} damage!")
        self._show_text(self.opponent, f"{attack_creature.display_name} used {skill.display_name} on {defend_creature.display_name} for {final_damage} damage!")

        if defend_creature.hp == 0:
            self._show_text(self.player, f"{defend_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defend_creature.display_name} fainted!")
            self.force_swap(defender)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} swapped to {choice.thing.display_name}!")
            self._show_text(self.opponent, f"{player.display_name} swapped to {choice.thing.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    @staticmethod
    def get_type_factor(skill_type: str, creature_type: str) -> float:
        type_chart = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 0.5, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 0.5}
        }
        return type_chart.get(skill_type, {}).get(creature_type, 1)
