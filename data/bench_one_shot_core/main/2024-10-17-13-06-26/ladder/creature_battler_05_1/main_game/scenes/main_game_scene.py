from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        if self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name if self.player.active_creature else 'No active creature'} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} if self.player.active_creature else 'N/A')
{self.opponent.display_name}: {self.opponent.active_creature.display_name if self.opponent.active_creature else 'No active creature'} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} if self.opponent.active_creature else 'N/A')

> Attack
> Swap
"""

    def run(self):
        while True:
            if self.check_battle_end():
                break
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            self.resolve_turn(player_action, opponent_action)

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        if self.player.active_creature.hp > 0:
            return self.get_player_action(self.player)
        else:
            return self.force_swap(self.player)

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        if self.opponent.active_creature.hp > 0:
            return self.get_player_action(self.opponent)
        else:
            return self.force_swap(self.opponent)

    def get_player_action(self, acting_player):
        while True:
            choices = []
            if acting_player.active_creature.hp > 0:
                choices.append(Button("Attack"))
            if self.has_available_creatures(acting_player):
                choices.append(Button("Swap"))
            
            if not choices:
                return None

            choice = self._wait_for_choice(acting_player, choices)

            if choice.display_name == "Attack":
                action = self.get_attack_action(acting_player)
                if action:
                    return action
            elif choice.display_name == "Swap":
                action = self.get_swap_action(acting_player)
                if action:
                    return action

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in acting_player.active_creature.skills]
        skill_choices.append(Button("Back"))
        choice = self._wait_for_choice(acting_player, skill_choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def get_swap_action(self, acting_player):
        available_creatures = [creature for creature in acting_player.creatures if creature != acting_player.active_creature and creature.hp > 0]
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        creature_choices.append(Button("Back"))
        choice = self._wait_for_choice(acting_player, creature_choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def has_available_creatures(self, player):
        return any(creature.hp > 0 and creature != player.active_creature for creature in player.creatures)

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort actions based on speed (or randomly if speeds are equal)
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for acting_player, action in actions:
            defending_player = self.opponent if acting_player == self.player else self.player
            self.execute_action(acting_player, defending_player, action)

    def execute_action(self, acting_player, defending_player, action):
        if isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)
            # Apply queued skill damage if the opponent chose to attack
            opponent_action = self.player_action if acting_player == self.opponent else self.opponent_action
            if isinstance(opponent_action.thing, Skill):
                self.execute_attack(defending_player, acting_player, opponent_action.thing)
        elif isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have fainted. {self.opponent.display_name} wins!")
            self.end_battle(self.opponent)
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You win!")
            self.end_battle(self.player)
            return True
        return False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            return choice
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")
            return None

    def end_battle(self, winner):
        self._show_text(self.player, f"The battle has ended. {winner.display_name} is the winner!")
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        self.reset_creatures()

        if play_again_button == choice:
            self._transition_to_scene("MainMenuScene")
        elif quit_button == choice:
            self._quit_whole_game()

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
