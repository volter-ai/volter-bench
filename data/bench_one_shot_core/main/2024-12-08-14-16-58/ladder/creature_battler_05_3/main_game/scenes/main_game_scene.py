from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset player creatures' HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
            
        # Reset bot creatures' HP    
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures = "\n".join(
            f"{'>' if c == self.player.active_creature else ' '} {c.display_name} - HP: {c.hp}/{c.max_hp}"
            for c in self.player.creatures
        )
        bot_creatures = "\n".join(
            f"{'>' if c == self.bot.active_creature else ' '} {c.display_name} - HP: {c.hp}/{c.max_hp}"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Creatures:
{player_creatures}

Opponent's Creatures:
{bot_creatures}

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.handle_turn(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self.handle_turn(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

    def handle_turn(self, current_player):
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
                    
                return ("attack", skill_choice.thing)

            elif choice == swap_button:
                # Show available creatures
                available_creatures = [
                    c for c in current_player.creatures 
                    if c != current_player.active_creature and c.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Opponent switched to {bot_action[1].display_name}!")

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1]))
            
        # Sort by speed with random tiebreaker
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        # Execute attacks
        for attacker, defender, skill in actions:
            self.execute_skill(attacker, defender, skill)
            
            # Force swap if needed
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(defender, creature_choices)
                    defender.active_creature = choice.thing
                    self._show_text(self.player, 
                        f"{'You' if defender == self.player else 'Opponent'} switched to {choice.thing.display_name}!")

    def execute_skill(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
            
        self._show_text(self.player, 
            f"{'You' if attacker == self.player else 'Opponent'} used {skill.display_name}! {effectiveness_text}")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
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
