from dataclasses import dataclass
from typing import Optional, Dict, List
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

@dataclass
class QueuedAction:
    player: Player
    action_type: str  # "attack" or "swap"
    skill: Optional[Skill] = None
    new_creature: Optional[Creature] = None

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        
        # Initialize battle state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Type: {player_creature.creature_type}
Stats: ATK {player_creature.attack} DEF {player_creature.defense} SP.ATK {player_creature.sp_attack} SP.DEF {player_creature.sp_defense} SPD {player_creature.speed}

Opponent's {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}
Type: {opponent_creature.creature_type}
Stats: ATK {opponent_creature.attack} DEF {opponent_creature.defense} SP.ATK {opponent_creature.sp_attack} SP.DEF {opponent_creature.sp_defense} SPD {opponent_creature.speed}

> Attack
> Swap"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Get player and opponent actions
            player_action = self._handle_player_turn(self.player)
            opponent_action = self._handle_player_turn(self.opponent)
            
            # Resolve actions
            self._resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _handle_player_turn(self, current_player: Player) -> QueuedAction:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                
                if skill_choice == back_button:
                    continue
                    
                return QueuedAction(
                    player=current_player,
                    action_type="attack",
                    skill=skill_choice.thing
                )
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [
                    c for c in current_player.creatures 
                    if c != current_player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    self._show_text(current_player, "No creatures available to swap!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                creature_choice = self._wait_for_choice(current_player, creature_choices)
                
                if creature_choice == back_button:
                    continue
                    
                return QueuedAction(
                    player=current_player,
                    action_type="swap",
                    new_creature=creature_choice.thing
                )

    def _resolve_turn(self, player_action: QueuedAction, opponent_action: QueuedAction):
        # Handle swaps first
        actions = [player_action, opponent_action]
        for action in actions:
            if action.action_type == "swap":
                self._perform_swap(action.player, action.new_creature)
        
        # Then handle attacks based on speed
        attack_actions = [a for a in actions if a.action_type == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            first = attack_actions[0]
            second = attack_actions[1]
            if second.player.active_creature.speed > first.player.active_creature.speed:
                first, second = second, first
            elif second.player.active_creature.speed == first.player.active_creature.speed:
                # Random order on speed tie
                if random.random() < 0.5:
                    first, second = second, first
                    
            for action in [first, second]:
                if action.player.active_creature.hp > 0:  # Only attack if still conscious
                    self._execute_attack(action)
        elif len(attack_actions) == 1:
            self._execute_attack(attack_actions[0])

    def _perform_swap(self, player: Player, new_creature: Creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(player, f"{old_creature.display_name} was swapped out for {new_creature.display_name}!")

    def _execute_attack(self, action: QueuedAction):
        attacker = action.player.active_creature
        defender = self.opponent.active_creature if action.player == self.player else self.player.active_creature
        skill = action.skill
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        # Show result
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(action.player, 
            f"{attacker.display_name} used {skill.display_name}! {effectiveness}\n"
            f"Dealt {final_damage} damage to {defender.display_name}!")
        
        # Handle KO
        if defender.hp == 0:
            self._show_text(action.player, f"{defender.display_name} was knocked out!")
            self._handle_knockout(defender.player)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, knocked_out_player: Player):
        # Check for available creatures
        available_creatures = [c for c in knocked_out_player.creatures if c.hp > 0]
        
        if not available_creatures:
            winner = self.player if knocked_out_player == self.opponent else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._quit_whole_game()
            return
            
        # Force swap
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(knocked_out_player, "Choose a new creature!")
        choice = self._wait_for_choice(knocked_out_player, creature_choices)
        self._perform_swap(knocked_out_player, choice.thing)

    def _check_battle_end(self) -> bool:
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            winner = self.player if opponent_alive else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            return True
            
        return False
