from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        self.selected_actions = {}

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_turn(self.player)
            if self.check_battle_end():
                break
            self.foe_turn(self.opponent)
            if self.check_battle_end():
                break
            self.resolution_phase()

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue
                self.selected_actions[current_player.uid] = ("attack", skill_choice.thing)
                break
            elif swap_button == choice:
                swap_result = self.swap_creature(current_player, allow_back=True)
                if swap_result == "back":
                    continue
                self.selected_actions[current_player.uid] = ("swap", swap_result)
                break

    def foe_turn(self, foe):
        while True:
            if random.random() < 0.8:  # 80% chance to attack
                skill = random.choice(foe.active_creature.skills)
                self.selected_actions[foe.uid] = ("attack", skill)
                break
            else:
                swap_result = self.swap_creature(foe, allow_back=False)
                if swap_result != "back":
                    self.selected_actions[foe.uid] = ("swap", swap_result)
                    break

    def swap_creature(self, player, allow_back=False):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        if not available_creatures:
            self._show_text(player, "No other creatures available to swap!")
            return None
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        if allow_back:
            back_button = Button("Back")
            creature_choices.append(back_button)
        
        choice = self._wait_for_choice(player, creature_choices)
        
        if choice == back_button:
            return "back"
        
        new_creature = choice.thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        return new_creature

    def resolution_phase(self):
        players = [self.player, self.opponent]
        random.shuffle(players)  # Randomize order for speed tie
        
        # Execute swap actions first
        for player in players:
            action, target = self.selected_actions.get(player.uid, (None, None))
            if action == "swap":
                player.active_creature = target

        # Then execute attack actions
        for player in players:
            action, target = self.selected_actions.get(player.uid, (None, None))
            if action == "attack":
                self.execute_attack(player, target)
            self.check_and_swap_if_fainted(player)

        self.selected_actions.clear()

    def execute_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neutral against all types
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_and_swap_if_fainted(self, player):
        if player.active_creature.hp == 0:
            self._show_text(self.player, f"{player.active_creature.display_name} has fainted!")
            self.swap_creature(player, allow_back=False)

    def check_battle_end(self) -> bool:
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
