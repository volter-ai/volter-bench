from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
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
            player_action = self._get_player_action(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._get_player_action(self.bot)
            if not bot_action:
                return

            # Resolve actions
            self._resolve_actions(player_action, bot_action)

            # Check for battle end
            self._check_battle_end()

    def _get_player_action(self, player):
        if self._needs_forced_swap(player):
            return self._force_swap(player)

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_attack_choice(self, player):
        creature = player.active_creature
        skill_choices = [SelectThing(skill) for skill in creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return self._get_player_action(player)
        
        return {"type": "attack", "skill": choice.thing}

    def _handle_swap_choice(self, player):
        available_creatures = [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return self._get_player_action(player)
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return self._get_player_action(player)
            
        return {"type": "swap", "creature": choice.thing}

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]

        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            # Determine order
            first = self.player
            second = self.bot
            first_action = p_action
            second_action = b_action
            
            if (self.bot.active_creature.speed > self.player.active_creature.speed or 
                (self.bot.active_creature.speed == self.player.active_creature.speed and 
                 random.random() < 0.5)):
                first = self.bot
                second = self.player
                first_action = b_action
                second_action = p_action

            self._execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self._execute_attack(second, first, second_action["skill"])

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)

        # Apply type effectiveness
        factor = self._get_type_effectiveness(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(
            attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!"
        )
        self._show_text(
            defender,
            f"{defender.active_creature.display_name} took {final_damage} damage!"
        )

    def _get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def _needs_forced_swap(self, player):
        return (player.active_creature.hp <= 0 and 
                any(c.hp > 0 for c in player.creatures if c != player.active_creature))

    def _force_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return None
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        return {"type": "swap", "creature": choice.thing}

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, 
                          "You win!" if winner == self.player else "You lose!")
            self._quit_whole_game()  # <-- This is the key fix
            return True
            
        return False
