from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Opponent's Team:
{self._format_team(self.opponent)}
"""

    def _format_team(self, player: Player) -> str:
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            self.current_player_action = self._handle_turn(self.player)
            if not self.current_player_action:
                return
                
            # Opponent turn
            self.current_opponent_action = self._handle_turn(self.opponent)
            if not self.current_opponent_action:
                return
                
            # Resolve actions
            self._resolve_actions(self.current_player_action, self.current_opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player: Player) -> dict:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_actions(self, player_action: dict, opponent_action: dict):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]
            self._show_text(self.player, f"Opponent switched to {opponent_action['creature'].display_name}!")

        # Then handle attacks
        first_action, second_action = self._determine_action_order(player_action, opponent_action)
        self._execute_action(first_action)
        self._execute_action(second_action)

    def _determine_action_order(self, player_action: dict, opponent_action: dict):
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return player_action, opponent_action
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            return opponent_action, player_action
        else:
            if random.random() < 0.5:
                return player_action, opponent_action
            return opponent_action, player_action

    def _execute_action(self, action: dict):
        if action["type"] != "attack":
            return
            
        # Determine attacker/defender based on which stored action this is
        if action == self.current_player_action:
            attacker = self.player
            defender = self.opponent
        else:
            attacker = self.opponent
            defender = self.player
        
        skill = action["skill"]
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._handle_knockout(defender)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def _handle_knockout(self, player: Player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            winner = self.player if player == self.opponent else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not opponent_has_creatures:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
