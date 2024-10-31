from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random
import time


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
            self.opponent_turn()
            self.resolve_turn()
            
            if self.check_battle_end():
                break

        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")

        time.sleep(2)
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

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
                back_button = Button("Back")
                creature_choices.append(back_button)
                if creature_choices:
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    if creature_choice == back_button:
                        continue
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
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, creature))
            else:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def resolve_turn(self):
        def sort_key(action):
            if action[0] == "swap":
                return -1
            return action[1].active_creature.speed

        # Sort the turn queue, with explicit handling for equal speeds
        self.turn_queue.sort(key=lambda x: (sort_key(x), random.random()), reverse=True)

        for action, player, target in self.turn_queue:
            opponent = self.opponent if player == self.player else self.player
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"Swapped to {target.display_name}!")
                self._show_text(opponent, f"Opponent swapped to {target.display_name}!")
            elif action == "attack":
                damage = self.calculate_damage(player.active_creature, opponent.active_creature, target)
                opponent.active_creature.hp = max(0, opponent.active_creature.hp - damage)
                self._show_text(player, f"{player.active_creature.display_name} used {target.display_name}!")
                self._show_text(opponent, f"Opponent's {player.active_creature.display_name} used {target.display_name}!")
                self._show_text(player, f"Dealt {damage} damage!")
                self._show_text(opponent, f"Took {damage} damage!")

                if opponent.active_creature.hp == 0:
                    self._show_text(player, f"Opponent's {opponent.active_creature.display_name} fainted!")
                    self._show_text(opponent, f"{opponent.active_creature.display_name} fainted!")
                    self.force_swap(opponent)

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

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Swapped to {player.active_creature.display_name}!")
            self._show_text(self.opponent if player == self.player else self.player, f"Opponent swapped to {player.active_creature.display_name}!")

    def check_battle_end(self) -> bool:
        return all(creature.hp == 0 for creature in self.player.creatures) or all(creature.hp == 0 for creature in self.opponent.creatures)

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
