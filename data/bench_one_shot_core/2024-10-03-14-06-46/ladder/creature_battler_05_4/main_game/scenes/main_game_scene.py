from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player_action = None
        self.opponent_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            self._player_turn()
            self._opponent_turn()
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self):
        while True:
            action_choice = self._wait_for_choice(self.player, [Button("Attack"), Button("Swap")])
            if action_choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    self.player_action = ("attack", skill_choice.thing)
                    break
            elif action_choice.display_name == "Swap":
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                creature_choice = self._wait_for_choice(self.player, creature_choices + [Button("Back")])
                if isinstance(creature_choice, SelectThing):
                    self.player_action = ("swap", creature_choice.thing)
                    break

    def _opponent_turn(self):
        opponent_creature = self.opponent.active_creature
        if opponent_creature.hp <= 0:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0]
            if available_creatures:
                self.opponent_action = ("swap", random.choice(available_creatures))
        else:
            if random.random() < 0.8:  # 80% chance to attack
                self.opponent_action = ("attack", random.choice(opponent_creature.skills))
            else:
                available_creatures = [c for c in self.opponent.creatures if c != opponent_creature and c.hp > 0]
                if available_creatures:
                    self.opponent_action = ("swap", random.choice(available_creatures))
                else:
                    self.opponent_action = ("attack", random.choice(opponent_creature.skills))

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        self._execute_action(*first)
        if self._check_battle_end():
            return
        self._execute_action(*second)

    def _determine_turn_order(self):
        player_speed = self.player.active_creature.speed
        opponent_speed = self.opponent.active_creature.speed
        if player_speed > opponent_speed or (player_speed == opponent_speed and random.random() < 0.5):
            return (self.player, self.player_action), (self.opponent, self.opponent_action)
        else:
            return (self.opponent, self.opponent_action), (self.player, self.player_action)

    def _execute_action(self, actor: Player, action):
        action_type, action_data = action
        if action_type == "swap":
            actor.active_creature = action_data
            self._show_text(self.player, f"{actor.display_name} swapped to {action_data.display_name}!")
        elif action_type == "attack":
            attacker = actor.active_creature
            defender = self.player.active_creature if actor == self.opponent else self.opponent.active_creature
            skill = action_data
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} and dealt {damage} damage to {defender.display_name}!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp <= 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
