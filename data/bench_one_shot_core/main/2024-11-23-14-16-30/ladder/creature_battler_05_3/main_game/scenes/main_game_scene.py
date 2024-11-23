from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Store initial hp values using prototype_ids as keys
        self.initial_player_hp = {creature.prototype_id: creature.max_hp for creature in self.player.creatures}
        self.initial_bot_hp = {creature.prototype_id: creature.max_hp for creature in self.bot.creatures}
        
    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = self.initial_player_hp[creature.prototype_id]
        for creature in self.bot.creatures:
            creature.hp = self.initial_bot_hp[creature.prototype_id]
        self.player.active_creature = None
        self.bot.active_creature = None

    def run(self):
        try:
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
                    break
        finally:
            # Always reset creatures when leaving the scene
            self.reset_creatures()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Determine order based on speed
        if player_action[0] == "swap" and bot_action[0] != "swap":
            first, second = player_action, bot_action
        elif bot_action[0] == "swap" and player_action[0] != "swap":
            first, second = bot_action, player_action
        else:
            # Compare speeds for attack order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = player_action, bot_action
            elif self.bot.active_creature.speed > self.player.active_creature.speed:
                first, second = bot_action, player_action
            else:
                # Random if speeds are equal
                if random.random() < 0.5:
                    first, second = player_action, bot_action
                else:
                    first, second = bot_action, player_action
                    
        # Execute actions
        self.execute_action(first)
        if self.check_battle_end():
            return
        self.execute_action(second)

    def execute_action(self, action):
        action_type, thing = action
        
        if action_type == "swap":
            if action[1] in self.player.creatures:
                self.player.active_creature = thing
                self._show_text(self.player, f"Go {thing.display_name}!")
            else:
                self.bot.active_creature = thing
                self._show_text(self.bot, f"Foe sends out {thing.display_name}!")
                
        elif action_type == "attack":
            skill = thing
            attacker = self.player if skill in self.player.active_creature.skills else self.bot
            defender = self.bot if attacker == self.player else self.player
            
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

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
