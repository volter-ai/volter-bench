from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}

> Attack
> Swap
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                self._quit_whole_game()
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()
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
            return {"type": "swap", "creature": choice.thing}
            
        while True:  # Main choice loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue  # Go back to main menu
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            else:  # Swap chosen
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available_creatures:
                    continue  # No valid swaps, return to main menu
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue  # Go back to main menu
                    
                player.active_creature = creature_choice.thing
                return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
        if bot_action["type"] == "swap":
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")
            
        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, player_action["skill"], self.bot))
        if bot_action["type"] == "attack":
            actions.append((self.bot, bot_action["skill"], self.player))
            
        # Sort by speed with randomization for ties
        def get_speed_key(action):
            return action[0].active_creature.speed
            
        if len(actions) == 2:
            speed1 = get_speed_key(actions[0])
            speed2 = get_speed_key(actions[1])
            if speed1 == speed2:
                # Randomize order for equal speeds
                random.shuffle(actions)
            else:
                # Sort by speed if different
                actions.sort(key=get_speed_key, reverse=True)
        
        for attacker, skill, defender in actions:
            damage = self._calculate_damage(attacker.active_creature, skill, defender.active_creature)
            defender.active_creature.hp -= damage
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.active_creature.display_name}!")

    def _calculate_damage(self, attacker, skill, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
