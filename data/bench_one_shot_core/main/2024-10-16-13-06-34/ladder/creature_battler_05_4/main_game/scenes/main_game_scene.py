from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.opponent.display_name}'s {opponent_creature.display_name if opponent_creature else 'No creature'}: HP {opponent_creature.hp}/{opponent_creature.max_hp if opponent_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_turn()
            self._opponent_turn()
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature and self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def _opponent_turn(self):
        choices = ["attack", "swap"]
        choice = random.choice(choices)

        if choice == "attack" and self.opponent.active_creature and self.opponent.active_creature.skills:
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, new_creature))
            elif self.opponent.active_creature and self.opponent.active_creature.skills:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def _resolve_turn(self):
        def sort_key(action):
            action_type, player, _ = action
            if action_type == "swap":
                return (-1, random.random())
            elif player.active_creature:
                return (player.active_creature.speed, random.random())
            else:
                return (0, random.random())

        self.turn_queue.sort(key=sort_key, reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack" and player.active_creature and self._get_opponent(player).active_creature:
                attacker = player.active_creature
                defender = self._get_opponent(player).active_creature
                damage = self._calculate_damage(attacker, defender, target)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(player, f"{attacker.display_name} used {target.display_name} and dealt {damage} damage to {defender.display_name}!")

                if defender.hp == 0:
                    self._show_text(player, f"{defender.display_name} was knocked out!")
                    self._force_swap(self._get_opponent(player))

        self.turn_queue.clear()

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = self._choose_creature(player, available_creatures)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")
            else:
                self._show_text(player, f"{player.display_name} failed to swap creatures.")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures to swap!")

    def _check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _choose_skill(self, player: Player) -> Skill | None:
        if not player.active_creature or not player.active_creature.skills:
            return None
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player: Player, creatures=None) -> Creature | None:
        if creatures is None:
            creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not creatures:
            return None
        choices = [SelectThing(creature, label=f"{creature.display_name} (HP: {creature.hp}/{creature.max_hp})") for creature in creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _get_opponent(self, player: Player) -> Player:
        return self.opponent if player == self.player else self.player
