from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
{self.opponent.display_name}'s {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
{"> Swap" if self.has_valid_swap_targets(self.player) else ""}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After showing win/loss message, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def has_valid_swap_targets(self, player):
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def get_player_action(self, player):
        choices = [Button("Attack")]
        if self.has_valid_swap_targets(player):
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return ("attack", self._wait_for_choice(player, choices).thing)
        else:
            valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            choices = [SelectThing(creature) for creature in valid_creatures]
            return ("swap", self._wait_for_choice(player, choices).thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            
        # Determine order for attacks
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.opponent, opponent_action[1])
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                first, second = (self.opponent, opponent_action[1]), (self.player, player_action[1])
            else:
                actors = [(self.player, player_action[1]), (self.opponent, opponent_action[1])]
                random.shuffle(actors)
                first, second = actors
                
            self.execute_attack(first[0], first[1])
            if self.opponent.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.opponent
        else:
            defender = self.player
            
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.active_creature.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

        # Force swap if active creature is knocked out
        if defender.active_creature.hp == 0:
            valid_creatures = [c for c in defender.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(creature) for creature in valid_creatures]
                new_creature = self._wait_for_choice(defender, choices).thing
                defender.active_creature = new_creature
                self._show_text(self.player, f"{defender.display_name} sent out {new_creature.display_name}!")

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
