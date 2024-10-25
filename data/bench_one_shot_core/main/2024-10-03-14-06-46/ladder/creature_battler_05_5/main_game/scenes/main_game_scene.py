from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player_action = None
        self.opponent_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            self._player_choice_phase()
            self._opponent_choice_phase()
            self._resolution_phase()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if isinstance(skill_choice, Button) and skill_choice.display_name == "Back":
                    continue
                self.player_action = ("attack", skill_choice.thing)
                break
            elif choice == swap_button:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if isinstance(creature_choice, Button) and creature_choice.display_name == "Back":
                    continue
                self.player_action = ("swap", creature_choice.thing)
                break

    def _opponent_choice_phase(self):
        available_skills = self.opponent.active_creature.skills
        available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
        
        if random.random() < 0.2 and available_creatures:  # 20% chance to swap if possible
            self.opponent_action = ("swap", random.choice(available_creatures))
        else:
            self.opponent_action = ("attack", random.choice(available_skills))

    def _resolution_phase(self):
        actions = [
            (self.player, self.player_action),
            (self.opponent, self.opponent_action)
        ]
        
        # Sort actions: swaps first, then by speed
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed))
        
        for player, action in actions:
            if action[0] == "swap":
                self._perform_swap(player, action[1])
            elif action[0] == "attack":
                self._perform_attack(player, action[1])

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show attack result
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")
        
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")

    def _get_type_effectiveness(self, skill_type, creature_type):
        effectiveness_chart = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness_chart.get((skill_type, creature_type), 1)

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        # Reset creature HP
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
