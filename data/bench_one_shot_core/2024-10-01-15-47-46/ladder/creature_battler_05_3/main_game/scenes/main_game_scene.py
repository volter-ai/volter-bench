import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""
Player: {self.player.display_name}
Active Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})

Opponent: {self.opponent.display_name}
Active Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

1. Attack
2. Swap
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self._player_choice_phase(self.player)
            
            # Foe Choice Phase
            foe_action = self._player_choice_phase(self.opponent)
            
            # Resolution Phase
            self._resolution_phase(player_action, foe_action)
            
            # Check for battle end
            if self._check_battle_end():
                break

        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, player):
        choice = self._wait_for_choice(player, [Button("Attack"), Button("Swap")])
        
        if choice.display_name == "Attack":
            return self._choose_attack(player)
        elif choice.display_name == "Swap":
            return self._choose_swap(player)

    def _choose_attack(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        
        while True:
            choice = self._wait_for_choice(player, choices)
            if isinstance(choice, SelectThing):
                return ("attack", choice.thing)
            elif choice.display_name == "Back":
                return self._player_choice_phase(player)

    def _choose_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        
        while True:
            choice = self._wait_for_choice(player, choices)
            if isinstance(choice, SelectThing):
                return ("swap", choice.thing)
            elif choice.display_name == "Back":
                return self._player_choice_phase(player)

    def _resolution_phase(self, player_action, foe_action):
        actions = [
            (self.player, player_action),
            (self.opponent, foe_action)
        ]
        
        # Sort actions by speed (swap always goes first)
        actions.sort(key=lambda x: (
            0 if x[1][0] == "swap" else 1,
            -x[0].active_creature.speed,
            random.random()  # Random tiebreaker for equal speed
        ))
        
        for player, action in actions:
            if action[0] == "swap":
                self._perform_swap(player, action[1])
            elif action[0] == "attack":
                self._perform_attack(player, action[1])

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
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
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")
        
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._force_swap(defender)

    def _get_type_effectiveness(self, skill_type, creature_type):
        effectiveness_chart = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        # Explicitly handle Normal type's neutrality
        if skill_type == "normal" or creature_type == "normal":
            return 1
        return effectiveness_chart.get((skill_type, creature_type), 1)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        self._perform_swap(player, choice.thing)
        return True

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
