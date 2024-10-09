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
        self._reset_creatures()
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
        # Execute swap actions first
        for player, action_type, action in turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")

        # Then execute attack actions
        attack_queue = [(player, action) for player, action_type, action in turn_queue if action_type == "attack"]
        attack_queue.sort(key=lambda x: (-x[0].active_creature.speed, random.random()))

        for player, skill in attack_queue:
            self._execute_skill(player, skill)

    def _execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        
        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack + skill.base_damage - defender_creature.defense)
        else:
            raw_damage = float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense) * float(skill.base_damage)
        
        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._handle_knockout(defender)
        
        # Check if attacker's creature is also knocked out (e.g., from recoil damage)
        if attacker.active_creature.hp == 0:
            self._handle_knockout(attacker)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        if skill_type == "normal":
            return 1.0  # Normal type is neutral against all types
        return effectiveness.get((skill_type, creature_type), 1.0)

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
