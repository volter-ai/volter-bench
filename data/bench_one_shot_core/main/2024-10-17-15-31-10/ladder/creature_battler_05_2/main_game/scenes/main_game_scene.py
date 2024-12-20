from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}: {player_creature.display_name if player_creature else 'No active creature'} (HP: {player_creature.hp}/{player_creature.max_hp} if player_creature else 'N/A')
{self.opponent.display_name}: {opponent_creature.display_name if opponent_creature else 'No active creature'} (HP: {opponent_creature.hp}/{opponent_creature.max_hp} if opponent_creature else 'N/A')

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            
            if player_action and opponent_action:
                self.resolve_actions(player_action, opponent_action)
            
            if self.check_battle_end():
                break

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        return self.get_player_action(self.player)

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        return self.get_player_action(self.opponent)

    def get_player_action(self, acting_player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(acting_player, choices)

            if attack_button == choice:
                attack_choice = self.get_attack_choice(acting_player)
                if attack_choice:
                    return attack_choice
            elif swap_button == choice:
                swap_choice = self.get_swap_choice(acting_player)
                if swap_choice:
                    return swap_choice

    def get_attack_choice(self, acting_player: Player):
        if acting_player.active_creature:
            choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
            choices.append(Button("Back"))
            choice = self._wait_for_choice(acting_player, choices)
            if isinstance(choice, Button) and choice.display_name == "Back":
                return None
            return choice
        return None

    def get_swap_choice(self, acting_player: Player):
        available_creatures = [c for c in acting_player.creatures if c != acting_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, "No creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(acting_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort actions based on speed, with random tiebreaker
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        for acting_player, action in actions:
            defending_player = self.opponent if acting_player == self.player else self.player
            self.execute_action(acting_player, defending_player, action)

    def execute_action(self, acting_player: Player, defending_player: Player, action):
        if action is None:
            self._show_text(acting_player, f"{acting_player.display_name} couldn't take any action!")
            return

        if isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)
        elif isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        if attacker.active_creature and defender.active_creature:
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")
            if defender.active_creature.hp == 0:
                self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
                self.force_swap(defender)

    def execute_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            player.active_creature = random.choice(available_creatures)
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            player.active_creature = None
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, f"You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, f"You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
