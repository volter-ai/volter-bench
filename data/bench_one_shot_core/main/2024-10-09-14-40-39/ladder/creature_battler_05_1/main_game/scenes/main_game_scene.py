from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        turn_queue = []
        while True:
            turn_queue.clear()
            self._player_choice_phase(self.player, turn_queue)
            self._player_choice_phase(self.bot, turn_queue)
            self._resolution_phase(turn_queue)
            if self._check_battle_end():
                break
        self._reset_creatures()  # Explicitly reset creatures before transitioning
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_choice_phase(self, player, turn_queue):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    turn_queue.append((player, "attack", skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self, turn_queue):
        turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        for player, action_type, action in turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                self._execute_attack(player, action)

    def _execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2, ("fire", "water"): 1/2,  # Changed 0.5 to 1/2
            ("water", "fire"): 2, ("water", "leaf"): 1/2,  # Changed 0.5 to 1/2
            ("leaf", "water"): 2, ("leaf", "fire"): 1/2  # Changed 0.5 to 1/2
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def _check_battle_end(self):
        player_creatures_knocked_out = all(c.hp == 0 for c in self.player.creatures)
        bot_creatures_knocked_out = all(c.hp == 0 for c in self.bot.creatures)

        if player_creatures_knocked_out and bot_creatures_knocked_out:
            self._show_text(self.player, "The battle ended in a draw!")
            return True
        elif player_creatures_knocked_out:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif bot_creatures_knocked_out:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
