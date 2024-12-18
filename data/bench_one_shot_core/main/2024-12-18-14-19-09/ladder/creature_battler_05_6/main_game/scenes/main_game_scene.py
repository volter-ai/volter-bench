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

Your Team: {[c.display_name + f"({c.hp}/{c.max_hp}HP)" for c in self.player.creatures]}
Foe's Team: {[c.display_name + f"({c.hp}/{c.max_hp}HP)" for c in self.bot.creatures]}"""

    def run(self):
        while True:
            # Battle loop
            if not self._handle_knockouts():
                # Battle is over, transition back to main menu
                self._show_text(self.player, "Returning to main menu...")
                self._transition_to_scene("MainMenuScene")
                return
                
            # Player phase
            player_action = self._get_turn_action(self.player)
            
            # Bot phase  
            bot_action = self._get_turn_action(self.bot)
            
            # Resolution phase
            self._resolve_actions(player_action, bot_action)

    def _get_turn_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            while True:
                choices = [SelectThing(s) for s in player.active_creature.skills]
                choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, choices)
                if isinstance(choice, Button):
                    return self._get_turn_action(player)
                return {"type": "attack", "skill": choice.thing}
        else:
            while True:
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    return self._get_turn_action(player)
                    
                choices = [SelectThing(c) for c in available_creatures]
                choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, choices)
                if isinstance(choice, Button):
                    return self._get_turn_action(player)
                return {"type": "swap", "creature": choice.thing}

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
            self._show_text(self.player, f"Go {p_action['creature'].display_name}!")
            
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            self._show_text(self.player, f"Foe sends out {b_action['creature'].display_name}!")

        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            first = self.player
            second = self.bot
            first_action = p_action
            second_action = b_action
            
            # Speed check
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and 
                random.random() < 0.5):
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
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
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
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness_text}")

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
            
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def _handle_knockouts(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if not available_creatures:
                    winner = "You" if player == self.bot else "The opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    return False
                    
                choices = [SelectThing(c) for c in available_creatures]
                choice = self._wait_for_choice(player, choices)
                player.active_creature = choice.thing
                
        return True
