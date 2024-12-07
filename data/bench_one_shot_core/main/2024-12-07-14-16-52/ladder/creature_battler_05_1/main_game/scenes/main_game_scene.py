from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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

Your other creatures:
{self._format_bench(self.player)}

Foe's other creatures:
{self._format_bench(self.bot)}
"""

    def _format_bench(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)

    def _handle_turn(self, player):
        if self._check_game_over():
            return None
            
        if player.active_creature.hp <= 0:
            if not self._handle_forced_swap(player):
                return None
                
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player):
        skills = [SelectThing(s) for s in player.active_creature.skills]
        back = Button("Back")
        choice = self._wait_for_choice(player, skills + [back])
        
        if choice == back:
            return self._handle_turn(player)
        return {"type": "attack", "skill": choice.thing, "creature": player.active_creature}

    def _handle_swap(self, player):
        available = [c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0]
        if not available:
            self._show_text(player, "No creatures available to swap!")
            return self._handle_turn(player)
            
        choices = [SelectThing(c) for c in available]
        back = Button("Back")
        choice = self._wait_for_choice(player, choices + [back])
        
        if choice == back:
            return self._handle_turn(player)
            
        return {"type": "swap", "creature": choice.thing}

    def _handle_forced_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            winner = self.bot if player == self.player else self.player
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._reset_creature_states()
            self._transition_to_scene("MainMenuScene")
            return False
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        actions = []
        if p_action["type"] == "attack":
            actions.append((self.player, self.bot, p_action))
        if b_action["type"] == "attack":
            actions.append((self.bot, self.player, b_action))
            
        # Sort by speed, with random order for ties
        actions.sort(key=lambda x: (x[2]["creature"].speed, random.random()), reverse=True)
        
        for attacker, defender, action in actions:
            self._resolve_attack(attacker, defender, action["skill"])

    def _resolve_attack(self, attacker, defender, skill):
        target = defender.active_creature
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - target.defense)
        else:
            raw_damage = ((attacker.active_creature.sp_attack / target.sp_defense) * 
                         skill.base_damage)
                         
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        target.hp = max(0, target.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if factor > 1 else "It's not very effective..." if factor < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def _get_type_factor(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def _check_game_over(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._reset_creature_states()
                self._transition_to_scene("MainMenuScene")
                return True
        return False

    def _reset_creature_states(self):
        """Reset all creatures to their initial state"""
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = None
