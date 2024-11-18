from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                return self._handle_battle_end(winner=self.bot)
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                return self._handle_battle_end(winner=self.player)
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return None
            
            self._show_text(player, f"{player.active_creature.display_name} is knocked out!")
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return {"type": "swap", "creature": choice.thing}

        return self._handle_main_menu(player)

    def _handle_main_menu(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])

        if choice == attack_button:
            return self._handle_attack_menu(player)
        else:
            return self._handle_swap_menu(player)

    def _handle_attack_menu(self, player):
        # Create skill choices plus back button
        skill_choices = [SelectThing(s) for s in player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return self._handle_main_menu(player)
        else:
            return {"type": "attack", "skill": choice.thing}

    def _handle_swap_menu(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return self._handle_main_menu(player)
        
        # Create creature choices plus back button
        creature_choices = [SelectThing(c) for c in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return self._handle_main_menu(player)
        else:
            player.active_creature = choice.thing
            return {"type": "swap", "creature": choice.thing}

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
        if bot_action["type"] == "swap":
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, player_action))
        if bot_action["type"] == "attack":
            actions.append((self.bot, bot_action))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        for attacker, action in actions:
            defender = self.bot if attacker == self.player else self.player
            self._execute_attack(attacker, defender, action["skill"])

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}\n"
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

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
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            return self._handle_battle_end(winner)
            
        return False

    def _handle_battle_end(self, winner):
        self._show_text(self.player, f"{winner.display_name} wins!")
        
        if winner == self.player:
            # If player wins, go back to main menu
            self._transition_to_scene("MainMenuScene")
        else:
            # If player loses, end the game
            self._quit_whole_game()
