from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button, BotListener
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

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
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                self._show_text(player, f"{player.display_name} has no creatures left!")
                return None
                
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return ("swap", choice.thing)

        # For bots, skip the choice menu and just pick randomly
        if isinstance(player._listener, BotListener):
            if random.random() < 0.2 and len([c for c in player.creatures if c.hp > 0 and c != player.active_creature]) > 0:
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                chosen_creature = random.choice(available_creatures)
                player.active_creature = chosen_creature
                return ("swap", chosen_creature)
            else:
                chosen_skill = random.choice(player.active_creature.skills)
                return ("attack", chosen_skill)
            
        return self._handle_player_choice(player)

    def _handle_player_choice(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                action = self._handle_attack_choice(player)
                if action:
                    return action
            else:
                action = self._handle_swap_choice(player)
                if action:
                    return action

    def _handle_attack_choice(self, player):
        skill_choices = [SelectThing(s) for s in player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def _handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            self._show_text(player, "No other creatures available to swap!")
            return None
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        player.active_creature = choice.thing
        return ("swap", choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
        if bot_action[0] == "swap":
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")
            
        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Speed check for attack order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                pass
            elif self.bot.active_creature.speed > self.player.active_creature.speed:
                actions.reverse()
            else:
                if random.random() < 0.5:
                    actions.reverse()
                    
        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self._execute_attack(attacker, defender, action[1])

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
