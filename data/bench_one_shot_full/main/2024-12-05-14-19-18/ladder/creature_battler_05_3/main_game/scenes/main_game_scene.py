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
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue
                return choice
            else:
                # Show available creatures with Back option
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                
                back_button = Button("Back")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue
                return choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
            
        if isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            self.opponent.active_creature = opponent_action.thing

        # Then handle attacks
        first, second = self.get_action_order(player_action, opponent_action)
        self.execute_action(first)
        self.execute_action(second)

    def get_action_order(self, player_action, opponent_action):
        p_speed = self.player.active_creature.speed
        o_speed = self.opponent.active_creature.speed
        
        if p_speed > o_speed or (p_speed == o_speed and random.random() < 0.5):
            return player_action, opponent_action
        return opponent_action, player_action

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return  # Skip if it's a swap
            
        skill = action.thing
        attacker = self.player.active_creature if action == self.player else self.opponent.active_creature
        defender = self.opponent.active_creature if action == self.player else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def reset_creatures(self):
        # Reset HP of all creatures to their max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self):
        p_has_active = any(c.hp > 0 for c in self.player.creatures)
        o_has_active = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not p_has_active:
            self._show_text(self.player, "You lost!")
            self.reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
        elif not o_has_active:
            self._show_text(self.player, "You won!")
            self.reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
