from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.current_phase = "player_choice"
        self.player_action = None
        self.bot_action = None
        
        # Reset creature HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        phase_info = {
            "player_choice": "=== Your Turn ===\nChoose your action:",
            "foe_choice": "=== Foe's Turn ===\nFoe is choosing...",
            "resolution": "=== Turn Resolution ==="
        }
        
        return f"""{phase_info.get(self.current_phase, '=== Battle ===')}
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

{"> Attack" if self.current_phase == "player_choice" else ""}
{"> Swap" if self.current_phase == "player_choice" else ""}"""

    def run(self):
        battle_ongoing = True
        while battle_ongoing:
            # Player Choice Phase
            self.current_phase = "player_choice"
            self.player_action = self.get_player_action(self.player)
            if not self.player_action:
                continue
                
            # Foe Choice Phase
            self.current_phase = "foe_choice"
            self.bot_action = self.get_bot_action()
            
            # Resolution Phase
            self.current_phase = "resolution"
            self.resolve_turn()
            
            # Check for battle end
            if self.check_battle_end():
                self._show_text(self.player, "Returning to main menu...")
                self._transition_to_scene("MainMenuScene")
                battle_ongoing = False

    def resolve_turn(self):
        # Handle swaps first (they always happen before attacks)
        if self.player_action["type"] == "swap":
            self.player.active_creature = self.player_action["creature"]
            self._show_text(self.player, f"You swapped to {self.player_action['creature'].display_name}!")
            
        if self.bot_action["type"] == "swap":
            self.bot.active_creature = self.bot_action["creature"]
            self._show_text(self.player, f"Foe swapped to {self.bot_action['creature'].display_name}!")

        # Then handle attacks
        if self.player_action["type"] == "attack" and self.bot_action["type"] == "attack":
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            # Determine order based on speed, with random tiebreaker
            if player_speed > bot_speed:
                first, second = self.player, self.bot
                first_action, second_action = self.player_action, self.bot_action
            elif bot_speed > player_speed:
                first, second = self.bot, self.player
                first_action, second_action = self.bot_action, self.player_action
            else:
                # Random tiebreaker for equal speed
                if random.random() < 0.5:
                    first, second = self.player, self.bot
                    first_action, second_action = self.player_action, self.bot_action
                else:
                    first, second = self.bot, self.player
                    first_action, second_action = self.bot_action, self.player_action
            
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action["skill"])

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.choose_attack(player)
        else:
            return self.choose_swap(player)

    def choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def choose_swap(self, player):
        available_creatures = [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return self.get_player_action(player)
            
        choices = [SelectThing(c) for c in available_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def get_bot_action(self):
        # Simple bot AI - randomly attack or swap
        if random.random() < 0.8:  # 80% chance to attack
            return {"type": "attack", "skill": random.choice(self.bot.active_creature.skills)}
        else:
            available_creatures = [
                c for c in self.bot.creatures 
                if c != self.bot.active_creature and c.hp > 0
            ]
            if available_creatures:
                return {"type": "swap", "creature": random.choice(available_creatures)}
            return {"type": "attack", "skill": random.choice(self.bot.active_creature.skills)}

    def execute_attack(self, attacker, defender, skill):
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
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness} {final_damage} damage!")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.handle_faint(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if player == self.player:
            self._show_text(self.player, "Choose your next creature!")
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"Foe sent out {player.active_creature.display_name}!")

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
