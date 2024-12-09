from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        
        # Reset creatures
        for p in [self.player, self.opponent]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.opponent
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Get player actions
            p1_action = self.get_player_action(self.player)
            p2_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(p1_action, p2_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            return self.force_swap(player)
            
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back = Button("Back")
        choice = self._wait_for_choice(player, choices + [back])
        
        if choice == back:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not valid_creatures:
            return self.get_player_action(player)
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        back = Button("Back")
        choice = self._wait_for_choice(player, choices + [back])
        
        if choice == back:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def force_swap(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return None
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        choice = self._wait_for_choice(player, choices)
        return {"type": "swap", "creature": choice.thing}

    def get_action_order(self, p1_action, p2_action, p1, p2):
        """Helper method to determine action order based on speed, with random resolution for ties"""
        # Swaps always go first
        if p1_action["type"] == "swap" and p2_action["type"] != "swap":
            return [(p1_action, p1, p2), (p2_action, p2, p1)]
        if p2_action["type"] == "swap" and p1_action["type"] != "swap":
            return [(p2_action, p2, p1), (p1_action, p1, p2)]
            
        # For attacks or double-swaps, compare speeds
        speed1 = p1.active_creature.speed
        speed2 = p2.active_creature.speed
        
        if speed1 == speed2:
            # Random order for speed ties
            actions = [(p1_action, p1, p2), (p2_action, p2, p1)]
            random.shuffle(actions)
            return actions
        elif speed1 > speed2:
            return [(p1_action, p1, p2), (p2_action, p2, p1)]
        else:
            return [(p2_action, p2, p1), (p1_action, p1, p2)]

    def resolve_turn(self, p1_action, p2_action):
        if not p1_action or not p2_action:
            return

        # Get action order based on speed and randomization for ties
        action_order = self.get_action_order(p1_action, p2_action, self.player, self.opponent)

        # Handle all actions in determined order
        for action, attacker, defender in action_order:
            if action["type"] == "swap":
                attacker.active_creature = action["creature"]
                self._show_text(attacker, f"{attacker.display_name} swapped to {action['creature'].display_name}!")
            elif action["type"] == "attack":
                self.resolve_attack(action["skill"], attacker, defender)

    def resolve_attack(self, skill, attacker, defender):
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
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
