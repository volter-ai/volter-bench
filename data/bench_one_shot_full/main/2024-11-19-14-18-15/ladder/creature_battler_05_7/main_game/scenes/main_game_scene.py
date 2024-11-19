from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Handle one full battle turn
            battle_result = self._handle_battle_turn()
            
            # Check if battle should end
            if battle_result:
                if battle_result == "player_win":
                    self._show_text(self.player, "You won the battle!")
                else:
                    self._show_text(self.player, "You lost the battle!")
                self._transition_to_scene("MainMenuScene")

    def _handle_battle_turn(self):
        """Handles one full turn of battle. Returns None if battle continues,
        'player_win' if player won, or 'player_lose' if player lost"""
        # Player turn
        player_action = self._handle_turn(self.player)
        if not player_action:
            return "player_lose"
            
        # Bot turn
        bot_action = self._handle_turn(self.bot)
        if not bot_action:
            return "player_win"
            
        # Resolve actions
        self._resolve_actions(player_action, bot_action)
        
        # Check for battle end
        return self._check_battle_end()

    def _handle_turn(self, player):
        if self._needs_to_swap(player):
            return self._force_swap(player)
            
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back = Button("Back")
        choices.append(back)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back:
            return self._handle_turn(player)
            
        return {"type": "attack", "skill": choice.thing, "creature": player.active_creature}

    def _handle_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available:
            return None
            
        choices = [SelectThing(c) for c in available]
        back = Button("Back")
        choices.append(back)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back:
            return self._handle_turn(player)
            
        return {"type": "swap", "new_creature": choice.thing}

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["new_creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["new_creature"]
            
        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, player_action))
        if bot_action["type"] == "attack":
            actions.append((self.bot, bot_action))
            
        # Sort by speed
        actions.sort(key=lambda x: x[1]["creature"].speed, reverse=True)
        
        for attacker, action in actions:
            defender = self.bot if attacker == self.player else self.player
            self._execute_attack(action["skill"], action["creature"], defender.active_creature)

    def _execute_attack(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _needs_to_swap(self, player):
        return player.active_creature.hp <= 0

    def _force_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return None
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        return {"type": "swap", "new_creature": choice.thing}

    def _check_battle_end(self):
        """Returns None if battle continues, 'player_win' if player won, 
        or 'player_lose' if player lost"""
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive:
            return "player_lose"
        elif not bot_alive:
            return "player_win"
            
        return None
