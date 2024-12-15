from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Add Back button for human players
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                if player == self.player:  # Only add Back for human player
                    back_button = Button("Back")
                    choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, choices)
                if skill_choice == back_button:
                    continue  # Go back to main choice
                return skill_choice
            else:
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not valid_creatures:
                    return None
                
                choices = [SelectThing(creature) for creature in valid_creatures]
                if player == self.player:  # Only add Back for human player
                    back_button = Button("Back")
                    choices.append(back_button)
                
                swap_choice = self._wait_for_choice(player, choices)
                if swap_choice == back_button:
                    continue  # Go back to main choice
                return swap_choice

    def force_swap(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return False
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        swap_choice = self._wait_for_choice(player, choices)
        player.active_creature = swap_choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You sent out {self.player.active_creature.display_name}!")
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe sent out {self.bot.active_creature.display_name}!")
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        
        # Check if we need forced swap before second action
        if self.player.active_creature.hp <= 0:
            if not self.force_swap(self.player):
                return
        if self.bot.active_creature.hp <= 0:
            if not self.force_swap(self.bot):
                return
                
        self.execute_action(second)
        
        # Check for forced swaps after second action
        if self.player.active_creature.hp <= 0:
            if not self.force_swap(self.player):
                return
        if self.bot.active_creature.hp <= 0:
            if not self.force_swap(self.bot):
                return

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return
            
        skill = action.thing
        attacker = self.player.active_creature if action in self.player.active_creature.skills else self.bot.active_creature
        defender = self.bot.active_creature if action in self.player.active_creature.skills else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
