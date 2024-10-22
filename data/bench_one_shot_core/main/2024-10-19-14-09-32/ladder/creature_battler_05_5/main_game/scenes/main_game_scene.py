from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.battle_ended = False

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}:
HP: {player_creature.hp}/{player_creature.max_hp if player_creature else 'N/A'}

{self.opponent.display_name}'s {opponent_creature.display_name if opponent_creature else 'No active creature'}:
HP: {opponent_creature.hp}/{opponent_creature.max_hp if opponent_creature else 'N/A'}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while not self.battle_ended:
            self.turn_counter += 1
            player_action = self._player_choice_phase(self.player)
            opponent_action = self._player_choice_phase(self.opponent)
            self._resolution_phase(player_action, opponent_action)
            
            if self._check_battle_end():
                self.battle_ended = True
        
        self._end_battle()

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature and self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            choices = [attack_button]
            
            if self._has_creatures_to_swap(player):
                swap_button = Button("Swap")
                choices.append(swap_button)
            
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                return self._choose_attack(player)
            elif swap_button == choice:
                return self._choose_swap(player)

    def _has_creatures_to_swap(self, player):
        return any(c for c in player.creatures if c != player.active_creature and c.hp > 0)

    def _choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        return self._wait_for_choice(player, choices)

    def _choose_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        if not choices:
            self._show_text(player, f"{player.display_name} has no creatures available to swap!")
            return self._choose_attack(player)
        return self._wait_for_choice(player, choices)

    def _resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort actions based on speed (swap actions go first)
        actions.sort(key=lambda x: (
            isinstance(x[1].thing, Creature),
            x[0].active_creature.speed
        ), reverse=True)

        for actor, action in actions:
            if isinstance(action.thing, Creature):
                self._perform_swap(actor, action.thing)
            elif isinstance(action.thing, Skill):
                self._perform_attack(actor, action.thing)

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self._force_swap(defender)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = available_creatures[0]
            self._perform_swap(player, new_creature)
        else:
            player.active_creature = None

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False

    def _end_battle(self):
        self._show_text(self.player, "Battle has ended!")
        return_button = Button("Return to Main Menu")
        choice = self._wait_for_choice(self.player, [return_button])
        if choice == return_button:
            self._transition_to_scene("MainMenuScene")
