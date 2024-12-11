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

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn - ensure we always get a valid action
            bot_action = self.get_bot_action()
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After showing win/loss message, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            
            if choice == back_button:
                return None
            return {"type": "attack", "skill": choice.thing}
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            
            if choice == back_button:
                return None
            return {"type": "swap", "creature": choice.thing}

    def get_bot_action(self):
        """Get a valid action for the bot - never returns None"""
        # If current creature is low on HP and we have other creatures, consider swapping
        if (self.bot.active_creature.hp < self.bot.active_creature.max_hp * 0.3):
            available_creatures = [c for c in self.bot.creatures 
                                if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return {"type": "swap", "creature": random.choice(available_creatures)}
        
        # Otherwise always attack with a random skill
        return {"type": "attack", "skill": random.choice(self.bot.active_creature.skills)}

    def resolve_turn(self, player_action, bot_action):
        # Both actions should be valid at this point
        assert player_action is not None
        assert bot_action is not None
        
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {bot_action['creature'].display_name}!")

        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, self.bot, player_action["skill"]))
        if bot_action["type"] == "attack":
            actions.append((self.bot, self.player, bot_action["skill"]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, defender, skill in actions:
            self.execute_attack(attacker, defender, skill)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    if defender == self.player:
                        choices = [SelectThing(c) for c in available_creatures]
                        choice = self._wait_for_choice(defender, choices)
                        defender.active_creature = choice.thing
                    else:
                        defender.active_creature = available_creatures[0]

    def execute_attack(self, attacker, defender, skill):
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
        effectiveness = self.get_type_effectiveness(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * effectiveness)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
