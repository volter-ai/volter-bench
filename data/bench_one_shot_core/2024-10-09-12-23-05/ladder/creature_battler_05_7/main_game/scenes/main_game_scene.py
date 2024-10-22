import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_queue = []

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
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.bot)
            self._resolution_phase()

            if self._check_battle_end():
                break

            self._handle_simultaneous_knockouts()

        self._show_battle_result()
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player):
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
        skill_choices = [SelectThing(skill) for skill in skills]
        skill_choices.append(Button("Back"))
        choice = self._wait_for_choice(player, skill_choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        creature_choices.append(Button("Back"))
        choice = self._wait_for_choice(player, creature_choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                if player.active_creature.hp > 0:
                    self._execute_skill(player, action)
                else:
                    self._show_text(player, f"{player.display_name}'s {player.active_creature.display_name} is knocked out and cannot attack!")

        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._handle_knockout(defender)

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)  # Return 1 for neutral effectiveness

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        self._force_swap(player)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self._choose_swap_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
            else:
                self._end_battle(player)
        else:
            self._end_battle(player)

    def _handle_simultaneous_knockouts(self):
        if self.player.active_creature.hp == 0 and self.bot.active_creature.hp == 0:
            self._show_text(self.player, "Both active creatures were knocked out!")
            self._force_swap(self.player)
            self._force_swap(self.bot)

    def _end_battle(self, loser):
        winner = self.bot if loser == self.player else self.player
        self._show_text(self.player, f"{winner.display_name} won the battle!")
        self._show_text(self.bot, f"{winner.display_name} won the battle!")

    def _check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        return not (player_has_creatures and bot_has_creatures)

    def _show_battle_result(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        if player_has_creatures:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
