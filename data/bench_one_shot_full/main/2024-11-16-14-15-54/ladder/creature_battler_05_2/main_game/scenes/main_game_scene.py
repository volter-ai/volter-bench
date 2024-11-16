from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
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

> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Player turn
            player_action = None
            while player_action is None:
                player_action = self.get_player_action(self.player)
                
            # Bot turn
            bot_action = None
            while bot_action is None:
                bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, current_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            skill_choices.append(back_button)
            skill_choice = self._wait_for_choice(current_player, skill_choices)
            
            if skill_choice == back_button:
                return None
            return {"type": "attack", "skill": skill_choice.thing}
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in current_player.creatures 
                                if c != current_player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(current_player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(back_button)
            creature_choice = self._wait_for_choice(current_player, creature_choices)
            
            if creature_choice == back_button:
                return None
            return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {bot_action['creature'].display_name}!")
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            first = self.player if self.player.active_creature.speed >= self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
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
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness = "super effective!" if multiplier > 1 else "not very effective..." if multiplier < 1 else ""
        owner = "Your" if attacker == self.player else "Foe's"
        self._show_text(self.player, 
            f"{owner} {attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            owner = "Your" if defender == self.player else "Foe's"
            self._show_text(self.player, f"{owner} {defender.active_creature.display_name} fainted!")
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
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            owner = "You" if player == self.player else "Foe"
            self._show_text(self.player, f"{owner} sent out {available_creatures[0].display_name}!")
        else:
            self._show_text(self.player, "Choose next creature:")
            creature_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            owner = "You" if player == self.player else "Foe"
            self._show_text(self.player, f"{owner} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = "You win!" if bot_has_creatures else "You lose!"
            self._show_text(self.player, winner)
            self._transition_to_scene("MainMenuScene")
            return True
        return False
