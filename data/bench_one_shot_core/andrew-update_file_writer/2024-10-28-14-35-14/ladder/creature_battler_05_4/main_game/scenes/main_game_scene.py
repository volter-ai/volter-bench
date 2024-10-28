from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self._get_creature(self.player.active_creature_id)
        opponent_creature = self._get_creature(self.opponent.active_creature_id)
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_turn()
            if self._check_battle_end():
                break
            self._opponent_turn()
            if self._check_battle_end():
                break
            self._resolve_turn()

    def _initialize_battle(self):
        self.player.active_creature_id = self.player.creature_ids[0]
        self.opponent.active_creature_id = self.opponent.creature_ids[0]

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
                new_creature_id = self._choose_creature(self.player)
                if new_creature_id:
                    self.turn_queue.append(("swap", self.player, new_creature_id))
                    break

    def _opponent_turn(self):
        choice = random.choice(["attack", "swap"])
        if choice == "attack":
            active_creature = self._get_creature(self.opponent.active_creature_id)
            skill = random.choice(active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill))
        else:
            available_creature_ids = [c_id for c_id in self.opponent.creature_ids if c_id != self.opponent.active_creature_id and self._get_creature(c_id).hp > 0]
            if available_creature_ids:
                new_creature_id = random.choice(available_creature_ids)
                self.turn_queue.append(("swap", self.opponent, new_creature_id))
            else:
                active_creature = self._get_creature(self.opponent.active_creature_id)
                skill = random.choice(active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else self._get_creature(x[1].active_creature_id).speed), reverse=True)
        
        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature_id = target
                creature = self._get_creature(target)
                self._show_text(player, f"{player.display_name} swapped to {creature.display_name}!")
            elif action == "attack":
                self._resolve_attack(player, target)

        self.turn_queue.clear()

    def _resolve_attack(self, attacker: Player, skill: Skill):
        defender = self.player if attacker == self.opponent else self.opponent
        attacker_creature = self._get_creature(attacker.active_creature_id)
        defender_creature = self._get_creature(defender.active_creature_id)
        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if all(self._get_creature(c_id).hp == 0 for c_id in self.player.creature_ids):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(self._get_creature(c_id).hp == 0 for c_id in self.opponent.creature_ids):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _choose_skill(self, player: Player) -> Skill | None:
        active_creature = self._get_creature(player.active_creature_id)
        skills = [create_from_game_database(skill_id, Skill) for skill_id in active_creature.skills]
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player: Player) -> str | None:
        available_creature_ids = [c_id for c_id in player.creature_ids if c_id != player.active_creature_id and self._get_creature(c_id).hp > 0]
        if not available_creature_ids:
            self._show_text(player, "No other creatures available to swap!")
            return None
        choices = [SelectThing(c_id, label=f"{self._get_creature(c_id).display_name} (HP: {self._get_creature(c_id).hp}/{self._get_creature(c_id).max_hp})") for c_id in available_creature_ids]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _get_creature(self, creature_id: str) -> Creature:
        return create_from_game_database(creature_id, Creature)
