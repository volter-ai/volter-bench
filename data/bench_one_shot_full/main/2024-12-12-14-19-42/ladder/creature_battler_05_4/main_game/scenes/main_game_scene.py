from typing import Dict, List, Optional, Tuple
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_actions: Dict[str, Tuple[str, Optional[Skill], Optional[Creature]]] = {}

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

Your options:
> Attack
> Swap
"""

    def reset_creatures_state(self, player: Player):
        """Reset all creatures back to their original state"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def run(self):
        self._show_text(self.player, "Battle Start!")
        while True:
            # Player Choice Phase
            self.handle_player_turn(self.player)
            
            # Foe Choice Phase
            self.handle_player_turn(self.opponent)
            
            # Resolution Phase
            self.resolve_turn()
            
            # Check for battle end
            if self.check_battle_end():
                # Reset state before leaving scene
                self.reset_creatures_state(self.player)
                self.reset_creatures_state(self.opponent)
                self._quit_whole_game()

    def handle_player_turn(self, current_player: Player):
        if current_player.active_creature.hp <= 0:
            self.force_swap(current_player)
            return

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            self.handle_attack_choice(current_player)
        elif choice == swap_button:
            self.handle_swap_choice(current_player)

    def handle_attack_choice(self, player: Player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            self.handle_player_turn(player)
        else:
            self.turn_actions[player.prototype_id] = ("attack", choice.thing, None)

    def handle_swap_choice(self, player: Player):
        available_creatures = [
            creature for creature in player.creatures 
            if creature.hp > 0 and creature != player.active_creature
        ]
        
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            self.handle_player_turn(player)
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            self.handle_player_turn(player)
        else:
            self.turn_actions[player.prototype_id] = ("swap", None, choice.thing)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        
        return int(raw_damage * effectiveness)

    def resolve_turn(self):
        # Handle swaps first
        for player in [self.player, self.opponent]:
            action = self.turn_actions.get(player.prototype_id)
            if action and action[0] == "swap":
                player.active_creature = action[2]
                self._show_text(player, f"{player.display_name} swapped to {action[2].display_name}!")

        # Then handle attacks in speed order
        players = [self.player, self.opponent]
        players.sort(key=lambda p: p.active_creature.speed, reverse=True)
        
        for player in players:
            action = self.turn_actions.get(player.prototype_id)
            if action and action[0] == "attack":
                skill = action[1]
                target = self.opponent if player == self.player else self.player
                
                damage = self.calculate_damage(player.active_creature, target.active_creature, skill)
                target.active_creature.hp = max(0, target.active_creature.hp - damage)
                
                self._show_text(player, 
                    f"{player.active_creature.display_name} used {skill.display_name} "
                    f"and dealt {damage} damage to {target.active_creature.display_name}!")
                
                if target.active_creature.hp <= 0:
                    self._show_text(player, f"{target.active_creature.display_name} was knocked out!")
                    self.force_swap(target)

        self.turn_actions.clear()

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
