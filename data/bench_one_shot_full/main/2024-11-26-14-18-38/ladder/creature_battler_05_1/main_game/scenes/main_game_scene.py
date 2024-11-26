from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

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
                self._quit_whole_game()  # Fixed: Properly quit game when it's over
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                self._quit_whole_game()  # Fixed: Properly quit game when it's over
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
        available = [SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0]
        back = Button("Back")
        choice = self._wait_for_choice(player, available + [back])
        
        if choice == back:
            return self._handle_turn(player)
        return {"type": "swap", "creature": choice.thing}

    def _handle_forced_swap(self, player):
        available = [SelectThing(c) for c in player.creatures if c.hp > 0]
        if not available:
            self._show_text(player, f"{player.display_name} has no creatures left!")
            return False
            
        choice = self._wait_for_choice(player, available)
        player.active_creature = choice.thing
        return True

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]

        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            first, second = self._determine_order(p_action, b_action)
            self._execute_attack(first)
            if second["creature"].hp > 0:  # Only if target still alive
                self._execute_attack(second)

    def _determine_order(self, p_action, b_action):
        p_speed = p_action["creature"].speed
        b_speed = b_action["creature"].speed
        
        if p_speed > b_speed:
            return p_action, b_action
        elif b_speed > p_speed:
            return b_action, p_action
        else:
            return random.choice([(p_action, b_action), (b_action, p_action)])

    def _execute_attack(self, action):
        attacker = action["creature"]
        skill = action["skill"]
        defender = self.bot.active_creature if attacker == self.player.active_creature else self.player.active_creature

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * factor)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_game_over(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive:
            self._show_text(self.player, "You lost!")
            return True
        elif not b_alive:
            self._show_text(self.player, "You won!")
            return True
        return False
