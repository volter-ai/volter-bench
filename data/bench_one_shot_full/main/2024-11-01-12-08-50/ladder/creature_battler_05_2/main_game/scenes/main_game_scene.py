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
        self.reset_creatures_state()

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
                available_creatures = [c for c in self.player.creatures if c != self.player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(self.player, "No creatures available to swap!")
                    continue
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if creature_choice == back_button:
                    continue
                self.turn_queue.append(("swap", self.player, creature_choice.thing))
                break

    def opponent_turn(self):
        opponent_choice = self._wait_for_choice(self.opponent, [Button("Make Move")])
        if opponent_choice:
            if random.choice(["attack", "swap"]) == "attack":
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))
            else:
                available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
                if available_creatures:
                    creature = random.choice(available_creatures)
                    self.turn_queue.append(("swap", self.opponent, creature))
                else:
                    skill = random.choice(self.opponent.active_creature.skills)
                    self.turn_queue.append(("attack", self.opponent, skill))

    def resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else 0), reverse=True)
        
        attack_actions = [action for action in self.turn_queue if action[0] == "attack"]
        if len(attack_actions) == 2 and attack_actions[0][1].active_creature.speed == attack_actions[1][1].active_creature.speed:
            random.shuffle(attack_actions)
            self.turn_queue = [action for action in self.turn_queue if action[0] == "swap"] + attack_actions

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
                if defender.hp == 0:
                    self._show_text(self.player, f"{defender.display_name} was knocked out!")
                    self.force_swap(self.player if defender == self.player.active_creature else self.opponent)

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
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = creature_choice.thing
            self._show_text(self.player, f"{player.display_name} swapped to {player.active_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
