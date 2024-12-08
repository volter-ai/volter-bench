from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your other creatures:
{self._format_bench(self.player)}

Foe's other creatures:
{self._format_bench(self.bot)}
"""

    def _format_bench(self, player):
        return "\n".join(f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                        for c in player.creatures if c != player.active_creature)

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
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player):
        if not self._has_valid_creatures(player):
            self._show_text(self.player, f"{player.display_name} has no creatures left!")
            return None
            
        attack = Button("Attack")
        swap = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player):
        creature = player.active_creature
        choices = [SelectThing(skill) for skill in creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._handle_turn(player)
            
        return ("attack", choice.thing)

    def _handle_swap(self, player):
        valid_creatures = [c for c in player.creatures 
                         if c != player.active_creature and c.hp > 0]
        
        if not valid_creatures:
            self._show_text(player, "No valid creatures to swap to!")
            return self._handle_turn(player)
            
        choices = [SelectThing(c) for c in valid_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._handle_turn(player)
            
        return ("swap", choice.thing)

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]
            
        # Then handle attacks
        actions = [(self.player, p_action), (self.bot, b_action)]
        
        # Sort by speed for attack order
        if p_action[0] == "attack" and b_action[0] == "attack":
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                random.shuffle(actions)
                
        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self._execute_attack(attacker, defender, action[1])

    def _execute_attack(self, attacker, defender, skill):
        a_creature = attacker.active_creature
        d_creature = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = a_creature.attack + skill.base_damage - d_creature.defense
        else:
            raw_damage = (a_creature.sp_attack / d_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, d_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        d_creature.hp = max(0, d_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{a_creature.display_name} used {skill.display_name} on {d_creature.display_name} for {final_damage} damage!")

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _has_valid_creatures(self, player):
        return any(c.hp > 0 for c in player.creatures)

    def _check_battle_end(self):
        p_has_creatures = self._has_valid_creatures(self.player)
        b_has_creatures = self._has_valid_creatures(self.bot)
        
        if not p_has_creatures or not b_has_creatures:
            winner = self.player if p_has_creatures else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
