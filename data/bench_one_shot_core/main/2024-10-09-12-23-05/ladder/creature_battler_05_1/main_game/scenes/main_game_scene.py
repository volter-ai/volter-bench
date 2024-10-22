from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.bot.display_name}'s {bot_creature.display_name if bot_creature else 'No active creature'}: HP {bot_creature.hp}/{bot_creature.max_hp if bot_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        self.game_loop()

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.bot.active_creature and self.bot.creatures:
            self.bot.active_creature = self.bot.creatures[0]

    def game_loop(self):
        while True:
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self._resolution_phase()

            if self._check_battle_end():
                self._end_battle()
                break

    def player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
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

    def _get_action_priority(self, action):
        player, action_type, _ = action
        if action_type == "swap":
            return (float('inf'), random.random())  # Swaps always go first
        return (player.active_creature.speed, random.random())

    def _resolution_phase(self):
        # Sort actions based on speed and random tiebreaker
        sorted_actions = sorted(self.turn_queue, key=self._get_action_priority, reverse=True)

        for player, action_type, action in sorted_actions:
            if action_type == "swap":
                old_creature = player.active_creature
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped {old_creature.display_name} for {action.display_name}!")
            elif action_type == "attack":
                defender = self.bot if player == self.player else self.player
                self._execute_skill(player, defender, action)

        self.turn_queue.clear()

    def _execute_skill(self, attacker, defender, skill):
        attacker_creature = attacker.active_creature
        defender_creature = defender.active_creature

        self._apply_skill(attacker, defender, skill)

    def _apply_skill(self, attacker, defender, skill):
        attacker_creature = attacker.active_creature
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(type_factor * raw_damage)  # Explicitly convert to integer

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _get_type_factor(self, skill_type, creature_type):
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
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        self._show_text(self.player, "The battle has ended!")
        self._reset_battle_state()
        self._transition_to_scene("MainMenuScene")

    def _reset_battle_state(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = None
        self.bot.active_creature = None
