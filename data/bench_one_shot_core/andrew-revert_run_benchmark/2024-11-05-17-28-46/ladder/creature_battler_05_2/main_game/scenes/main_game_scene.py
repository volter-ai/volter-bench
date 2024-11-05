from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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
        self._show_text(self.opponent, "Battle start!")

        while True:
            self.player_turn()
            self.opponent_turn()
            self.resolve_turn()

            if self.check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                self.turn_queue.append(("attack", self.player, skill_choice.thing))
                break
            elif choice == swap_button:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature.hp > 0 and creature != self.player.active_creature]
                if creature_choices:
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    self.turn_queue.append(("swap", self.player, creature_choice.thing))
                    break
                else:
                    self._show_text(self.player, "No other creatures available to swap!")

    def opponent_turn(self):
        choices = ["attack", "swap"]
        choice = random.choice(choices)

        if choice == "attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill))
        elif choice == "swap":
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, creature))
            else:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                attacker = player.active_creature
                defender = self.opponent.active_creature if player == self.player else self.player.active_creature
                damage = self.calculate_damage(attacker, defender, target)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {target.display_name} on {defender.display_name} for {damage} damage!")
                self._show_text(self.opponent, f"{attacker.display_name} used {target.display_name} on {defender.display_name} for {damage} damage!")

                if defender.hp == 0:
                    self._show_text(self.player, f"{defender.display_name} fainted!")
                    self._show_text(self.opponent, f"{defender.display_name} fainted!")
                    self.force_swap(self.player if defender == self.player.active_creature else self.opponent)

        self.turn_queue.clear()

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        type_chart = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 0.5, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 0.5}
        }
        return type_chart.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} swapped to {choice.thing.display_name}!")
            self._show_text(self.opponent, f"{player.display_name} swapped to {choice.thing.display_name}!")

    def check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False
