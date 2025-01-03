from typing import Dict
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene[Player]):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app=app, player=player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Reset both players' creatures HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Opponent's Team:
{self._format_team(self.opponent)}"""

    def _format_team(self, player: Player) -> str:
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            opponent_action = self._get_player_action(self.opponent)
            
            self._resolve_actions(player_action, opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _get_player_action(self, player: Player) -> tuple:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._get_attack_choice(player)
        else:
            return self._get_swap_choice(player)

    def _get_attack_choice(self, player: Player) -> tuple:
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self._get_player_action(player)
        return ("attack", choice.thing)

    def _get_swap_choice(self, player: Player) -> tuple:
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self._get_player_action(player)
        return ("swap", choice.thing)

    def _resolve_actions(self, player_action: tuple, opponent_action: tuple):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            
        # Then handle attacks
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                self._execute_attack(self.player, player_action[1], self.opponent)
                if self.opponent.active_creature.hp > 0:
                    self._execute_attack(self.opponent, opponent_action[1], self.player)
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                self._execute_attack(self.opponent, opponent_action[1], self.player)
                if self.player.active_creature.hp > 0:
                    self._execute_attack(self.player, player_action[1], self.opponent)
            else:
                if random.random() < 0.5:
                    self._execute_attack(self.player, player_action[1], self.opponent)
                    if self.opponent.active_creature.hp > 0:
                        self._execute_attack(self.opponent, opponent_action[1], self.player)
                else:
                    self._execute_attack(self.opponent, opponent_action[1], self.player)
                    if self.player.active_creature.hp > 0:
                        self._execute_attack(self.player, player_action[1], self.opponent)

        self._handle_knockouts()

    def _execute_attack(self, attacker: Player, skill: Skill, defender: Player):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.active_creature.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def _handle_knockouts(self):
        for player in [self.player, self.opponent]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    choices = [SelectThing(c) for c in available_creatures]
                    self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
