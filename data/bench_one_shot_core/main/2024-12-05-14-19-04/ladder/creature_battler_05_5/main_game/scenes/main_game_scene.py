from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Reset all creatures to full HP when starting a new battle
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
{"> Swap" if self.has_valid_swaps(self.player) else ""}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Execute actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Instead of transitioning to menu, quit the game when it's over
                self._quit_whole_game()
                return

    def has_valid_swaps(self, player):
        return any(c != player.active_creature and c.hp > 0 for c in player.creatures)

    def get_player_action(self, player):
        while True:
            choices = [Button("Attack")]
            if self.has_valid_swaps(player):
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                action = self.get_attack_choice(player)
                if action:  # If not None (back wasn't selected)
                    return action
            elif choice.display_name == "Swap":
                action = self.get_swap_choice(player)
                if action:  # If not None (back wasn't selected)
                    return action

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return {"type": "attack", "skill": choice.thing}

    def get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]

        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, self.opponent, player_action["skill"]))
        if opponent_action["type"] == "attack":
            actions.append((self.opponent, self.player, opponent_action["skill"]))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        # Execute attacks
        for attacker, defender, skill in actions:
            self.execute_attack(attacker.active_creature, defender.active_creature, skill)
            if defender.active_creature.hp <= 0:
                self.handle_fainted_creature(defender)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)

        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            winner = self.player if player == self.opponent else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
        else:
            choices = [SelectThing(creature) for creature in available_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        return not (player_has_creatures and opponent_has_creatures)
