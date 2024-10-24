from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
        self._show_text(self.player, "A wild opponent appeared!")
        while True:
            self.player_turn()
            if self.check_battle_end():
                break
            self.opponent_turn()
            if self.check_battle_end():
                break
            self.resolution_phase()
            if self.check_battle_end():
                break

    def player_turn(self):
        while True:
            choices = []
            if self.player.active_creature.skills:
                choices.append(Button("Attack"))
            available_creatures = [c for c in self.player.creatures if c != self.player.active_creature and c.hp > 0]
            if available_creatures:
                choices.append(Button("Swap"))
            
            if not choices:
                self._show_text(self.player, f"{self.player.active_creature.display_name} has no available actions!")
                return

            choice = self._wait_for_choice(self.player, choices)

            if self.get_choice_value(choice) == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if self.get_choice_value(skill_choice) == "Back":
                    continue
                self.turn_queue.append(("attack", self.player, skill_choice.thing))
                break
            elif self.get_choice_value(choice) == "Swap":
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if self.get_choice_value(creature_choice) == "Back":
                    continue
                self.turn_queue.append(("swap", self.player, creature_choice.thing))
                break

    def get_choice_value(self, choice):
        if isinstance(choice, Button):
            return choice.display_name
        elif isinstance(choice, SelectThing):
            return choice.thing
        else:
            raise ValueError(f"Unexpected choice type: {type(choice)}")

    def opponent_turn(self):
        opponent_choice = self._wait_for_choice(self.opponent, [Button("Make Move")])
        if opponent_choice:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if self.opponent.active_creature.skills and (random.choice(["attack", "swap"]) == "attack" or not available_creatures):
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))
            elif available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, creature))
            else:
                self._show_text(self.player, f"{self.opponent.active_creature.display_name} has no available actions!")

    def resolution_phase(self):
        def action_priority(action):
            if action[0] == "swap":
                return (-1, 0)
            return (action[1].active_creature.speed, random.random())

        self.turn_queue.sort(key=action_priority, reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                attacker = player.active_creature
                defender = self.opponent.active_creature if player == self.player else self.player.active_creature
                damage = self.calculate_damage(attacker, defender, target)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {target.display_name} and dealt {damage} damage to {defender.display_name}!")
                
                # Check and force swap after each attack
                self.check_and_force_swap(self.player)
                self.check_and_force_swap(self.opponent)

        self.turn_queue.clear()

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def check_and_force_swap(self, player: Player):
        if player.active_creature.hp == 0:
            self._show_text(self.player, f"{player.active_creature.display_name} has been knocked out!")
            self.force_swap(player)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choice = self._wait_for_choice(player, creature_choices)
                new_creature = creature_choice.thing
            else:
                new_creature = random.choice(available_creatures)
            
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")
