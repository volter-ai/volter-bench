from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()
        
    def _reset_creatures(self):
        # Reset all creatures to full HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
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

    def _handle_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])

            if choice == attack_button:
                skills = current_player.active_creature.skills
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in skills] + [back_button]
                skill_choice = self._wait_for_choice(current_player, choices)
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice == swap_button:
                available_creatures = [c for c in current_player.creatures 
                                    if c != current_player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
                creature_choice = self._wait_for_choice(current_player, choices)
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.bot, f"Foe sends out {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
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
            
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness_text}")

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self._handle_fainted_creature(defender)

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def _handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature!")
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go {choice.thing.display_name}!")

    def _check_battle_end(self):
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
