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
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Execute actions
            self._resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _get_player_action(self, player):
        if self._needs_forced_swap(player):
            return self._force_swap(player)
            
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self._choose_attack(player)
        else:
            return self._choose_swap(player)

    def _choose_attack(self, player):
        skills = [Button(s.display_name) for s in player.active_creature.skills]
        back = Button("Back")
        choice = self._wait_for_choice(player, skills + [back])
        
        if choice == back:
            return self._get_player_action(player)
            
        return ("attack", player.active_creature.skills[skills.index(choice)])

    def _choose_swap(self, player):
        available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available:
            return self._get_player_action(player)
            
        choices = [SelectThing(c) for c in available]
        back = Button("Back")
        choice = self._wait_for_choice(player, choices + [back])
        
        if choice == back:
            return self._get_player_action(player)
            
        return ("swap", choice.thing)

    def _force_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return None
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        return ("swap", choice.thing)

    def _needs_forced_swap(self, player):
        return player.active_creature.hp <= 0

    def _resolve_turn(self, p_action, b_action):
        if not p_action or not b_action:
            return
            
        # Handle swaps first
        for action, player in [(p_action, self.player), (b_action, self.bot)]:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        actions = [(p_action, self.player, self.bot), (b_action, self.bot, self.player)]
        
        # Sort by speed
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if action[0] == "attack":
                self._execute_attack(action[1], attacker, defender)

    def _execute_attack(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._quit_whole_game()  # <-- Added this line to properly end the game
            return True
            
        return False
