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
        player_creature_info = f"{player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}" if player_creature else "No active creature"
        opponent_creature_info = f"{opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}" if opponent_creature else "No active creature"
        return f"""===Battle===
{self.player.display_name}'s {player_creature_info}
{self.opponent.display_name}'s {opponent_creature_info}

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

        self.end_battle()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choices = ["attack", "swap"]
        choice = random.choice(choices)

        if choice == "attack" and self.opponent.active_creature:
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, new_creature))
            elif self.opponent.active_creature:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed if x[1].active_creature else -2), reverse=True)

        for action in self.turn_queue:
            action_type, player, target = action
            if action_type == "swap":
                self.swap_creature(player, target)
            elif action_type == "attack" and player.active_creature:
                self.execute_attack(player, target)

        self.turn_queue.clear()

    def execute_attack(self, attacker: Player, skill: Skill):
        defender = self.player if attacker == self.opponent else self.opponent
        if not defender.active_creature:
            return

        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.active_creature.display_name} used {skill.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def swap_creature(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        if new_creature:
            self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
            self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures!")
            self._show_text(self.opponent, f"{player.display_name} has no more creatures!")

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self.choose_creature(player)
            self.swap_creature(player, new_creature)
        else:
            self.swap_creature(player, None)

    def choose_skill(self, player: Player) -> Skill:
        if not player.active_creature:
            return None
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def choose_creature(self, player: Player) -> Creature:
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def check_battle_end(self) -> bool:
        player_creatures_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_creatures_alive = any(c.hp > 0 for c in self.opponent.creatures)
        return not (player_creatures_alive and opponent_creatures_alive)

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = player.creatures[0]

    def end_battle(self):
        player_won = any(c.hp > 0 for c in self.player.creatures)
        if player_won:
            self._show_text(self.player, "Congratulations! You won the battle!")
            self._show_text(self.opponent, "You lost the battle.")
        else:
            self._show_text(self.player, "You lost the battle.")
            self._show_text(self.opponent, "Congratulations! You won the battle!")

        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")
