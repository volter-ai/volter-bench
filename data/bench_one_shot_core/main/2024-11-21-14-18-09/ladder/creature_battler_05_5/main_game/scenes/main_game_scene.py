from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
{self.opponent.display_name}'s {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

{self.player.display_name}'s {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal" or defender_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knocked_out(self, player, opponent):
        # Check if any player has all creatures knocked out
        player_has_alive = any(c.hp > 0 for c in player.creatures)
        opponent_has_alive = any(c.hp > 0 for c in opponent.creatures)

        if not player_has_alive:
            self._show_text(player, "You lost the battle!")
            return True
        elif not opponent_has_alive:
            self._show_text(player, "You won the battle!")
            return True

        # Force swap if active creature is knocked out
        if player.active_creature.hp <= 0:
            alive_creatures = [c for c in player.creatures if c.hp > 0]
            choice = self._wait_for_choice(player, [SelectThing(c) for c in alive_creatures])
            player.active_creature = choice.thing

        if opponent.active_creature.hp <= 0:
            alive_creatures = [c for c in opponent.creatures if c.hp > 0]
            choice = self._wait_for_choice(opponent, [SelectThing(c) for c in alive_creatures])
            opponent.active_creature = choice.thing

        return False

    def run(self):
        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            player_choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            player_action = None
            if player_choice == attack_button:
                skills = self.player.active_creature.skills
                back_button = Button("Back")
                skill_choices = [SelectThing(s) for s in skills] + [back_button]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice != back_button:
                    player_action = ("attack", skill_choice.thing)
            else:
                available_creatures = [c for c in self.player.creatures 
                                    if c != self.player.active_creature and c.hp > 0]
                back_button = Button("Back")
                creature_choices = [SelectThing(c) for c in available_creatures] + [back_button]
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if creature_choice != back_button:
                    player_action = ("swap", creature_choice.thing)

            if not player_action:
                continue

            # Opponent turn
            opponent_action = None
            if random.random() < 0.7:  # 70% chance to attack
                opponent_action = ("attack", random.choice(self.opponent.active_creature.skills))
            else:
                available_creatures = [c for c in self.opponent.creatures 
                                    if c != self.opponent.active_creature and c.hp > 0]
                if available_creatures:
                    opponent_action = ("swap", random.choice(available_creatures))
                else:
                    opponent_action = ("attack", random.choice(self.opponent.active_creature.skills))

            # Resolution phase
            actions = [(self.player, player_action), (self.opponent, opponent_action)]
            
            # Sort by speed for attacks
            if all(action[1][0] == "attack" for action in actions):
                actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
                if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                    random.shuffle(actions)

            # Execute actions
            for player, (action_type, target) in actions:
                other_player = self.opponent if player == self.player else self.player
                
                if action_type == "swap":
                    player.active_creature = target
                    self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
                else:  # attack
                    damage = self._calculate_damage(player.active_creature, other_player.active_creature, target)
                    other_player.active_creature.hp -= damage
                    self._show_text(player, 
                        f"{player.active_creature.display_name} used {target.display_name} "
                        f"and dealt {damage} damage!")

            # Check for knocked out creatures
            if self._handle_knocked_out(self.player, self.opponent):
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
