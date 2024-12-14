from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Available actions: {"Attack" if p_creature.hp > 0 else ""} {"Swap" if any(c.hp > 0 for c in self.player.creatures if c != p_creature) else ""}"""

    def run(self):
        try:
            while True:
                # Check for battle end before each turn
                if self.check_battle_end():
                    self._quit_whole_game()
                    return
                    
                # Get player actions if they can make moves
                player_action = self.get_player_action(self.player)
                if player_action is None:  # Player has no valid moves
                    self._show_text(self.player, f"{self.player.display_name} has no valid moves!")
                    self._quit_whole_game()
                    return
                    
                bot_action = self.get_player_action(self.bot)
                if bot_action is None:  # Bot has no valid moves
                    self._show_text(self.player, f"{self.bot.display_name} has no valid moves!")
                    self._quit_whole_game()
                    return
                
                # Resolve actions
                self.resolve_turn(player_action, bot_action)
        finally:
            # Reset creature states when leaving scene
            for p in [self.player, self.bot]:
                for c in p.creatures:
                    c.hp = c.max_hp
                p.active_creature = p.creatures[0]

    def get_player_action(self, player):
        while True:
            choices = self.get_available_choices(player)
            if not choices:
                return None
                
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Back":
                continue
            elif choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                if skill_choice.display_name == "Back":
                    continue
                return skill_choice
            else:  # Swap
                valid_creatures = [c for c in player.creatures 
                                 if c != player.active_creature and c.hp > 0]
                swaps = [SelectThing(creature) for creature in valid_creatures]
                swaps.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, swaps)
                if swap_choice.display_name == "Back":
                    continue
                return swap_choice

    def get_available_choices(self, player):
        choices = []
        
        # Can only attack if active creature has HP
        if player.active_creature.hp > 0:
            choices.append(Button("Attack"))
            
        # Can only swap if there are other creatures with HP
        if any(c.hp > 0 for c in player.creatures if c != player.active_creature):
            choices.append(Button("Swap"))
            
        return choices

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
                self._show_text(player, f"{player.display_name} swapped to {action.thing.display_name}!")

        # Then handle attacks in speed order
        actions = [(p1_action, self.player, self.bot), 
                  (p2_action, self.bot, self.player)]
        
        # Sort by speed, with random resolution for ties
        actions.sort(key=lambda x: (x[1].active_creature.speed, random.random()), reverse=True)
        
        for action, attacker, defender in actions:
            if not isinstance(action.thing, Creature):  # It's a skill
                damage = self.calculate_damage(action.thing, 
                                            attacker.active_creature,
                                            defender.active_creature)
                                            
                defender.active_creature.hp -= damage
                self._show_text(attacker, 
                    f"{attacker.active_creature.display_name} used {action.thing.display_name}!")
                self._show_text(defender,
                    f"{defender.active_creature.display_name} took {damage} damage!")
                
                if defender.active_creature.hp <= 0:
                    self.handle_knockout(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return max(1, int(raw_damage * multiplier))  # Minimum 1 damage

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            swap = self._wait_for_choice(player,
                [SelectThing(c) for c in valid_creatures])
            player.active_creature = swap.thing
            self._show_text(player, f"Go, {swap.thing.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(c.hp > 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, 
                    f"{winner.display_name} wins the battle!")
                return True
        return False
