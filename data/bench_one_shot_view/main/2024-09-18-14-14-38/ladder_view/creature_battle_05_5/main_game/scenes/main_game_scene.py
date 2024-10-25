from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
import time


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
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
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.bot)
            self._resolution_phase()
            if self._check_battle_end():
                break

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

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
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _resolution_phase(self):
        # Sort the turn queue based on action type, speed, and a random factor for equal speeds
        self.turn_queue.sort(key=lambda x: (
            x[1] != "swap",  # Swap actions go first
            -x[0].active_creature.speed,  # Higher speed goes first
            random.random()  # Random tiebreaker for equal speeds
        ))
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                self._execute_skill(player, action)
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
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self._force_swap(defender)

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

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
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            time.sleep(2)  # Give the player time to see the result
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            time.sleep(2)  # Give the player time to see the result
            self._transition_to_scene("MainMenuScene")
            return True
        return False
