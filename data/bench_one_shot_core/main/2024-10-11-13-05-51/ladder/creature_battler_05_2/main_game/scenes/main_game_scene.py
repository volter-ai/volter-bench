from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []
        self.battle_ended = False

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
        self._initialize_battle()
        while not self.battle_ended:
            self._player_turn()
            if not self.battle_ended:
                self._opponent_turn()
            if not self.battle_ended:
                self._resolve_turn()
            self._check_battle_end()
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self):
        while not self.battle_ended:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def _opponent_turn(self):
        choices = ["attack", "swap"]
        choice = random.choice(choices)

        if choice == "attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("attack", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, new_creature))
            else:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append(("attack", self.opponent, skill))

    def _resolve_turn(self):
        self.turn_queue.sort(key=self._get_action_priority, reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                self._swap_creature(player, target)
            elif action == "attack":
                self._execute_attack(player, target)
                self._check_and_force_swap(self.player if player == self.opponent else self.opponent)
                if self.battle_ended:
                    break

        self.turn_queue.clear()

    def _get_action_priority(self, action_tuple):
        action, player, target = action_tuple
        if action == "swap":
            return (2, 0)  # Swapping always goes first
        else:  # attack
            speed = player.active_creature.speed
            return (1, speed, random.random())  # Use random tiebreaker for equal speeds

    def _swap_creature(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _execute_attack(self, attacker: Player, skill: Skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _check_and_force_swap(self, player: Player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                if player == self.player:
                    new_creature = self._choose_creature(player)
                else:
                    new_creature = random.choice(available_creatures)
                if new_creature:
                    self._swap_creature(player, new_creature)
                else:
                    self._end_battle_with_winner(self.player if player == self.opponent else self.opponent)
            else:
                self._end_battle_with_winner(self.player if player == self.opponent else self.opponent)

    def _check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._end_battle_with_winner(self.opponent)
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._end_battle_with_winner(self.player)
        return self.battle_ended

    def _end_battle_with_winner(self, winner: Player):
        self.battle_ended = True
        self._show_text(self.player, f"{winner.display_name} won the battle!")

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _choose_skill(self, player: Player) -> Skill:
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.base_damage} dmg)") for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player: Player) -> Creature:
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=f"{creature.display_name} (HP: {creature.hp}/{creature.max_hp})") for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None
