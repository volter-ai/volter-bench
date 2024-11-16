from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Player
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
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue
            
            # Resolve actions only when both are valid
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            skill_choice = self._wait_for_choice(player, skill_choices)
            
            if skill_choice == back_button:
                return None
                
            return ("attack", skill_choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(back_button)
            creature_choice = self._wait_for_choice(player, creature_choices)
            
            if creature_choice == back_button:
                return None
                
            return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Both actions should be valid at this point
        assert player_action is not None and bot_action is not None
        
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe sends out {bot_action[1].display_name}!")
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, skill)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    if defender == self.player:
                        self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
                        creature_choices = [SelectThing(c) for c in available_creatures]
                        choice = self._wait_for_choice(defender, creature_choices)
                        defender.active_creature = choice.thing
                        self._show_text(defender, f"Go {choice.thing.display_name}!")
                    else:
                        defender.active_creature = available_creatures[0]
                        self._show_text(self.player, f"Foe's {defender.active_creature.display_name} fainted!")
                        self._show_text(self.player, f"Foe sends out {defender.active_creature.display_name}!")

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
            
        owner = "Your" if attacker == self.player else "Foe's"
        self._show_text(self.player, 
            f"{owner} {attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

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
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            
        return False
