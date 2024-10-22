from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent_creatures = self._create_opponent_creatures()
        self.opponent_active_creature = self.opponent_creatures[0]
        self.turn_queue = []
        self.battle_ended = False

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent_active_creature
        return f"""===Battle===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Opponent's {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while not self.battle_ended:
            self._player_choice_phase()
            self._opponent_choice_phase()
            self._resolution_phase()
            self.battle_ended = self._check_battle_end()
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self._show_text(self.player, f"You sent out {self.player.active_creature.display_name}!")
        self._show_text(self.player, f"Opponent sent out {self.opponent_active_creature.display_name}!")

    def _player_choice_phase(self):
        self._show_text(self.player, "It's your turn to make a choice.")
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self._choose_skill()
                if skill:
                    self.turn_queue.append(("player", "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature()
                if new_creature:
                    self.turn_queue.append(("player", "swap", new_creature))
                    break

    def _choose_skill(self):
        skills = self.player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(self.player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _choose_swap_creature(self):
        available_creatures = [c for c in self.player.creatures if c != self.player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(self.player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _opponent_choice_phase(self):
        available_skills = self.opponent_active_creature.skills
        chosen_skill = random.choice(available_skills)
        self.turn_queue.append(("opponent", "attack", chosen_skill))

    def _resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -self._get_creature_speed(x[0]), random.random()))
        for actor, action_type, action in self.turn_queue:
            if action_type == "swap":
                self._perform_swap(actor, action)
            elif action_type == "attack":
                self._perform_attack(actor, action)
        self.turn_queue.clear()

    def _get_creature_speed(self, actor):
        return self.player.active_creature.speed if actor == "player" else self.opponent_active_creature.speed

    def _perform_swap(self, actor, new_creature):
        if actor == "player":
            self.player.active_creature = new_creature
            self._show_text(self.player, f"You swapped to {new_creature.display_name}!")
        else:
            self.opponent_active_creature = new_creature
            self._show_text(self.player, f"Opponent swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        if attacker == "player":
            attacker_creature = self.player.active_creature
            defender_creature = self.opponent_active_creature
        else:
            attacker_creature = self.opponent_active_creature
            defender_creature = self.player.active_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(c.hp == 0 for c in self.opponent_creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        if self.player.active_creature.hp == 0:
            self._force_swap("player")
        if self.opponent_active_creature.hp == 0:
            self._force_swap("opponent")
        return False

    def _force_swap(self, actor):
        if actor == "player":
            available_creatures = [c for c in self.player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self._perform_swap("player", new_creature)
        else:
            available_creatures = [c for c in self.opponent_creatures if c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self._perform_swap("opponent", new_creature)

    def _end_battle(self):
        self._transition_to_scene("MainMenuScene")

    def _create_opponent_creatures(self):
        # Create a list of predefined opponent creatures
        return [
            Creature.from_prototype_id("scizard"),
            Creature.from_prototype_id("dumbird")
        ]
