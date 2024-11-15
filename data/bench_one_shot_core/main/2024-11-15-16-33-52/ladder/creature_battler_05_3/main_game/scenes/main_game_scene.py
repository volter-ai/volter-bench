from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your choices:
> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature HP before transitioning
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                choices = skill_choices + [back_button]
                
                skill_choice = self._wait_for_choice(player, choices)
                if skill_choice == back_button:
                    continue
                return skill_choice
            else:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap to!")
                    continue
                
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                choices = creature_choices + [back_button]
                
                creature_choice = self._wait_for_choice(player, choices)
                if creature_choice == back_button:
                    continue
                return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Opponent switched to {bot_action.thing.display_name}!")
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0].skills[0])):
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

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def check_battle_end(self):
        player_has_healthy = any(c.hp > 0 for c in self.player.creatures)
        bot_has_healthy = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_healthy:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_healthy:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
