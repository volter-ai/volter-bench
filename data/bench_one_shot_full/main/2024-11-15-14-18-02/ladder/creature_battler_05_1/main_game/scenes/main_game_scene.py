from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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

            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # <-- Added this line to properly end the game

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(back_button)
                choice = self._wait_for_choice(player, skill_choices)
                
                if choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": choice.thing}
                
            elif choice == swap_button:
                # Show available creatures
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available]
                creature_choices.append(back_button)
                choice = self._wait_for_choice(player, creature_choices)
                
                if choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
            self._show_text(self.player, f"Go {p_action['creature'].display_name}!")
            
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            self._show_text(self.player, f"Foe sends out {b_action['creature'].display_name}!")

        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            # Determine order
            first = self.player
            second = self.bot
            first_action = p_action
            second_action = b_action
            
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and random.random() < 0.5):
                first = self.bot
                second = self.player
                first_action = b_action
                second_action = p_action
                
            # Execute attacks
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action["skill"])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")
            
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_fainted_creature(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return
            
        self._show_text(self.player, "Choose next creature!")
        choice = self._wait_for_choice(player, [SelectThing(c) for c in available])
        player.active_creature = choice.thing

    def check_battle_end(self):
        p_available = any(c.hp > 0 for c in self.player.creatures)
        b_available = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_available:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not b_available:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
