from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap (if available)"""

    def run(self):
        while True:
            try:
                # Check for battle end before each turn
                if self.check_battle_end():
                    break
                    
                # Player turn
                player_action = self.get_player_action(self.player)
                if not player_action:  # No valid actions available
                    break
                    
                opponent_action = self.get_player_action(self.opponent)
                if not opponent_action:  # No valid actions available
                    break
                
                # Resolve actions
                self.resolve_turn(player_action, opponent_action)
                
            except Exception as e:
                # Reset creatures before re-raising
                self.reset_creatures()
                raise e
        
        # Reset creatures before ending
        self.reset_creatures()
        self._quit_whole_game()

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def get_available_swap_creatures(self, player):
        return [
            creature 
            for creature in player.creatures 
            if creature != player.active_creature and creature.hp > 0
        ]

    def get_player_action(self, player):
        while True:
            choices = []
            
            # Always offer Attack if creature has skills
            if player.active_creature and player.active_creature.skills:
                choices.append(Button("Attack"))
                
            # Only offer Swap if there are valid creatures to swap to
            available_creatures = self.get_available_swap_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
                
            if not choices:
                return None
                
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue  # Go back to main menu
                return skill_choice
                
            else:  # Swap
                # Show available creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue  # Go back to main menu
                return creature_choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            self.opponent.active_creature = opponent_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort by speed with random tiebreaker
        actions.sort(key=lambda x: (
            x[0].active_creature.speed,
            random.random()  # Random tiebreaker
        ), reverse=True)
        
        for actor, action in actions:
            if isinstance(action.thing, type(self.player.creatures[0].skills[0])):
                self.execute_skill(actor, action.thing)

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

        # Force swap if active creature is knocked out
        if defender.active_creature.hp == 0:
            available_creatures = self.get_available_swap_creatures(defender)
            if available_creatures:
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                choice = self._wait_for_choice(defender, swap_choices)
                defender.active_creature = choice.thing

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not has_available_creatures(self.opponent):
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
