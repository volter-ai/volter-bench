from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature, Skill
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
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._get_bot_action()
            if not bot_action:
                continue
                
            # Resolution phase
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")

    def _get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = player.active_creature.skills
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in skills] + [back_button]
                
                skill_choice = self._wait_for_choice(player, choices)
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
                
                creature_choice = self._wait_for_choice(player, choices)
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def _get_bot_action(self):
        # Simple bot AI - randomly choose between attack and swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return {"type": "attack", "skill": skill}
        else:
            available_creatures = [c for c in self.bot.creatures 
                                if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return {"type": "swap", "creature": random.choice(available_creatures)}
            else:
                skill = random.choice(self.bot.active_creature.skills)
                return {"type": "attack", "skill": skill}

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed, with random tiebreaker
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed == bot_speed:
                # Random selection when speeds are equal
                first = random.choice([self.player, self.bot])
            else:
                first = self.player if player_speed > bot_speed else self.bot
                
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
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
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
                       f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")
        
        # Handle knockout
        if defender.active_creature.hp <= 0:
            self._handle_knockout(defender)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if player == self.player:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = available_creatures[0]
            
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")

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
