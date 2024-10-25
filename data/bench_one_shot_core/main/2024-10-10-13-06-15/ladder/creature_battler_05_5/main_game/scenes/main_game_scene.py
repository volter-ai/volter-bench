from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        self._initialize_battle()
        while True:
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
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif choice == swap_button:
                creature = self._choose_creature(self.player)
                if creature:
                    self.turn_queue.append(("swap", self.player, creature))
                    break

    def _opponent_turn(self):
        choices = ["Attack", "Swap"]
        choice = self._wait_for_choice(self.opponent, [Button(c) for c in choices])

        if choice.display_name == "Attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("skill", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, creature))

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (x[0] != "swap", -x[1].active_creature.speed))
        
        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "skill":
                self._execute_skill(player, target)

        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self._get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender_creature.display_name} fainted!")
            if not self._force_swap(defender):
                self._end_battle()

    def _get_type_effectiveness(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _force_swap(self, player):
        creature = self._choose_creature(player)
        if creature:
            player.active_creature = creature
            self._show_text(player, f"{player.display_name} sent out {creature.display_name}!")
            return True
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
            return False

    def _check_battle_end(self):
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

    def _choose_skill(self, player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return None
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None
