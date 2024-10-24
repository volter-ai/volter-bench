from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


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
            self.resolve_actions(player_action, opponent_action)
            battle_end, player_won = self.check_battle_end()
            if battle_end:
                self.end_battle(player_won)
                break
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                action = self.choose_attack(current_player)
            elif choice == swap_button:
                action = self.choose_swap(current_player)
            
            if action:
                return action
            else:
                self._show_text(current_player, "Invalid choice. Please try again.")

    def choose_attack(self, current_player):
        choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(current_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def choose_swap(self, current_player):
        choices = [SelectThing(creature) for creature in current_player.creatures 
                   if creature != current_player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        if not choices:
            self._show_text(current_player, "No creatures available to swap.")
            return None
        choice = self._wait_for_choice(current_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Prioritize swaps
        for player, action in actions:
            if isinstance(action.thing, Creature):
                self.execute_swap(player, action.thing)
        
        # Resolve attacks based on speed
        attacks = [(player, action) for player, action in actions if isinstance(action.thing, Skill)]
        attacks.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        if len(attacks) == 2 and attacks[0][0].active_creature.speed == attacks[1][0].active_creature.speed:
            random.shuffle(attacks)
        
        for attacker, action in attacks:
            defender = self.opponent if attacker == self.player else self.player
            self.execute_attack(attacker, defender, action.thing)
            if defender.active_creature.hp == 0:
                if not self.force_swap(defender):
                    break

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
        if all(creature.hp == 0 for creature in self.player.creatures):
            return True, False  # Battle ended, player lost
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            return True, True  # Battle ended, player won
        return False, False  # Battle not ended

    def end_battle(self, player_won):
        if player_won:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def force_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0]
        if not available_creatures:
            return False
        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(current_player, choices).thing
        self.execute_swap(current_player, new_creature)
        return True
