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
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.opponent)
            self._resolution_phase()
            
            if self._check_battle_end():
                break

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
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _resolution_phase(self):
        # Sort the turn queue, adding a random factor for equal speeds
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                self._execute_skill(player, action)
        
        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature
        
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)  # Explicitly convert to integer
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")
        
        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} was knocked out!")
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
        if not available_creatures:
            return
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def _check_battle_end(self):
        return all(c.hp == 0 for c in self.player.creatures) or all(c.hp == 0 for c in self.opponent.creatures)

    def _show_battle_result(self):
        if all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "Congratulations! You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle. Better luck next time!")

    def _reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
