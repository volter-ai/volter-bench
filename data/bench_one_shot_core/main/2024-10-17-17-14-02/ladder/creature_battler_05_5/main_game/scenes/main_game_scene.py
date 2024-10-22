from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
        battle_ended = False
        while not battle_ended:
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            self.resolve_actions(player_action, opponent_action)
            battle_ended, player_won = self.check_battle_end()

        if player_won:
            self._show_text(self.player, f"Congratulations! You've won the battle!")
        else:
            self._show_text(self.player, f"You've lost the battle. Better luck next time!")

        self.reset_creatures_state()
        self._quit_whole_game()

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        return self.get_player_action(self.player)

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        return self.get_player_action(self.opponent)

    def get_player_action(self, acting_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(acting_player, choices)

            if choice == attack_button:
                action = self.get_attack_action(acting_player)
            elif choice == swap_button:
                action = self.get_swap_action(acting_player)

            if action:
                return action

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
        back_button = Button("Back")
        skill_choices.append(back_button)
        choice = self._wait_for_choice(acting_player, skill_choices)
        if choice == back_button:
            return None
        return choice

    def get_swap_action(self, acting_player):
        available_creatures = [creature for creature in acting_player.creatures if creature != acting_player.active_creature and creature.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, f"No available creatures to swap to!")
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        choice = self._wait_for_choice(acting_player, creature_choices)
        if choice == back_button:
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort actions: swaps first, then by creature speed
        actions.sort(key=lambda x: (not isinstance(x[1].thing, Creature), -x[0].active_creature.speed))
        
        # Resolve ties randomly
        i = 0
        while i < len(actions) - 1:
            if actions[i][0].active_creature.speed == actions[i+1][0].active_creature.speed:
                if random.choice([True, False]):
                    actions[i], actions[i+1] = actions[i+1], actions[i]
            i += 1

        for acting_player, action in actions:
            defending_player = self.opponent if acting_player == self.player else self.player
            self.execute_action(acting_player, defending_player, action)

    def execute_action(self, acting_player, defending_player, action):
        if isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)
        elif isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)

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
        if skill_type == "normal" or defender_type == "normal":
            return 1  # Normal is neither effective nor ineffective against any type
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
            self._show_text(self.player, f"All your creatures have fainted. {self.opponent.display_name} wins!")
            return True, False
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You win!")
            return True, True
        elif self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        elif self.opponent.active_creature.hp == 0:
            self.force_swap(self.opponent)
        return False, False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} was forced to swap to {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
