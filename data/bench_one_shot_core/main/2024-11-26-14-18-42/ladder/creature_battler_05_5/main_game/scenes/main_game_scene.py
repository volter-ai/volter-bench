from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, current_player: Player) -> dict:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in current_player.creatures 
                                    if c != current_player.active_creature and c.hp > 0]
                
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_action: dict, bot_action: dict):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, self.bot, player_action["skill"]))
        if bot_action["type"] == "attack":
            actions.append((self.bot, self.player, bot_action["skill"]))
            
        # Sort by speed with random tiebreaker
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        # Execute attacks
        for attacker, defender, skill in actions:
            self.execute_attack(attacker, defender, skill)
            
            # Check if defender needs to swap
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    choice = self._wait_for_choice(defender, creature_choices)
                    defender.active_creature = choice.thing
                    self._show_text(self.player, 
                        f"{'You' if defender == self.player else 'Foe'} switched to {choice.thing.display_name}!")

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(self.player, 
            f"{'Your' if attacker == self.player else 'Foe'} {attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
