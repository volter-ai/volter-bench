from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset all creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your other creatures:
{self._format_bench_creatures(self.player)}

Foe's other creatures:
{self._format_bench_creatures(self.bot)}
"""

    def _format_bench_creatures(self, player):
        return "\n".join([f"- {c.display_name}: HP {c.hp}/{c.max_hp}" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Battle loop
            if not self._check_battle_end():
                # Player turn
                player_action = self._handle_turn_choices(self.player)
                # Bot turn  
                bot_action = self._handle_turn_choices(self.bot)
                # Resolve actions
                self._resolve_turn(player_action, bot_action)
            else:
                break

        self._transition_to_scene("MainMenuScene")

    def _check_battle_end(self):
        # Check if either player has all creatures knocked out
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_alive:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _handle_turn_choices(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choices = [attack, swap]
            
            choice = self._wait_for_choice(player, choices)
            
            if choice == attack:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if isinstance(skill_choice, Button):  # Back button
                    continue
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap:
                # Show available creatures
                available_creatures = [c for c in player.creatures 
                                    if c.hp > 0 and c != player.active_creature]
                if not available_creatures:
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, creature_choices)
                
                if isinstance(creature_choice, Button):  # Back button
                    continue
                return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You swapped to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe swapped to {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
            # Execute attacks in order
            self._execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:  # Only if target still alive
                self._execute_attack(second, first, second_action["skill"])

        # Force swap if any creature is knocked out
        self._handle_forced_swaps()

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

    def _get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def _handle_forced_swaps(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    if len(available_creatures) == 1:
                        player.active_creature = available_creatures[0]
                    else:
                        creature_choices = [SelectThing(c) for c in available_creatures]
                        choice = self._wait_for_choice(player, creature_choices)
                        player.active_creature = choice.thing
