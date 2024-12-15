from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize active creatures and reset their HP
        self.reset_player_creatures(self.player)
        self.reset_player_creatures(self.opponent)
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def reset_player_creatures(self, player):
        """Reset HP of all creatures to their max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp
        player.active_creature = None

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        if not self.has_valid_creatures(player):
            return None
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])

        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        choices = [SelectThing(creature) for creature in valid_creatures]
        back_button = Button("Back")
        choices.append(back_button)

        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action and player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You swapped to {player_action['creature'].display_name}!")
            
        if opponent_action and opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]
            self._show_text(self.player, f"Opponent swapped to {opponent_action['creature'].display_name}!")

        # Then handle attacks
        if player_action and opponent_action:
            actions = [(self.player, player_action), (self.opponent, opponent_action)]
            if player_action["type"] == "attack" and opponent_action["type"] == "attack":
                # Sort by speed
                actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
                if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                    random.shuffle(actions)
                    
            for attacker, action in actions:
                if action["type"] == "attack":
                    defender = self.opponent if attacker == self.player else self.player
                    self.execute_attack(attacker, defender, action["skill"])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        raw_damage = self.calculate_raw_damage(attacker.active_creature, defender.active_creature, skill)
        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name} on {defender.active_creature.display_name} for {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def calculate_raw_damage(self, attacker, defender, skill):
        if skill.is_physical:
            return attacker.attack + skill.base_damage - defender.defense
        else:
            return (attacker.sp_attack / defender.sp_defense) * skill.base_damage

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        if not self.has_valid_creatures(player):
            return
            
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        choices = [SelectThing(creature) for creature in valid_creatures]
        
        self._show_text(self.player, "Choose next creature!")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing

    def has_valid_creatures(self, player):
        return any(creature.hp > 0 for creature in player.creatures)

    def check_battle_end(self):
        if not self.has_valid_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            self.reset_player_creatures(self.player)
            self.reset_player_creatures(self.opponent)
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not self.has_valid_creatures(self.opponent):
            self._show_text(self.player, "You won the battle!")
            self.reset_player_creatures(self.player)
            self.reset_player_creatures(self.opponent)
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
