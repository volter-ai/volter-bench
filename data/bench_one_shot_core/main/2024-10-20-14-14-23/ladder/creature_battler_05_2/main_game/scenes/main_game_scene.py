from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            self.execute_turn(player_action, opponent_action)
            
            if self.check_battle_end():
                self.handle_battle_end()
                return

    def get_player_action(self, current_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == attack_button:
            return self.choose_attack(current_player)
        elif choice == swap_button:
            swap_action = self.choose_swap(current_player)
            if swap_action is None:
                self._show_text(current_player, "No creatures available to swap!")
                return self.get_player_action(current_player)  # Retry action selection
            return swap_action

    def choose_attack(self, current_player):
        choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        return self._wait_for_choice(current_player, choices)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
        if not available_creatures:
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        return self._wait_for_choice(current_player, choices)

    def execute_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort actions based on speed (swap actions always go first)
        actions.sort(key=lambda x: (
            not isinstance(x[1].thing, Creature),  # Swap actions first
            -x[0].active_creature.speed  # Then by speed (descending)
        ))
        
        for player, action in actions:
            if isinstance(action.thing, Skill):
                self.execute_attack(player, self.get_opponent(player), action.thing)
            elif isinstance(action.thing, Creature):
                self.execute_swap(player, action.thing)

    def get_opponent(self, player):
        return self.opponent if player == self.player else self.player

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self):
        return all(creature.hp == 0 for creature in self.player.creatures) or \
               all(creature.hp == 0 for creature in self.opponent.creatures)

    def handle_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

        self.reset_creatures()

        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return False
        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")
        return True
