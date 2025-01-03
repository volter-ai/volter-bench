from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
{self.player.display_name}'s {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
{self.bot.display_name}'s {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

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
                return

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
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
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
        # Determine order
        first_action = None
        second_action = None
        
        # Swaps go first
        if player_action[0] == "swap" and bot_action[0] != "swap":
            first_action = (self.player, player_action)
            second_action = (self.bot, bot_action)
        elif bot_action[0] == "swap" and player_action[0] != "swap":
            first_action = (self.bot, bot_action)
            second_action = (self.player, player_action)
        # Speed comparison for attacks
        else:
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first_action = (self.player, player_action)
                second_action = (self.bot, bot_action)
            elif self.bot.active_creature.speed > self.player.active_creature.speed:
                first_action = (self.bot, bot_action)
                second_action = (self.player, player_action)
            else:
                if random.random() < 0.5:
                    first_action = (self.player, player_action)
                    second_action = (self.bot, bot_action)
                else:
                    first_action = (self.bot, bot_action)
                    second_action = (self.player, player_action)
        
        # Execute actions
        self.execute_action(*first_action)
        if second_action[1][0] != "swap" or second_action[1][1].hp > 0:
            self.execute_action(*second_action)

    def execute_action(self, player, action):
        action_type, thing = action
        
        if action_type == "swap":
            player.active_creature = thing
            self._show_text(self.player, f"{player.display_name} swapped to {thing.display_name}!")
            
        elif action_type == "attack":
            skill = thing
            attacker = player.active_creature
            defender = self.bot.active_creature if player == self.player else self.player.active_creature
            
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
        # Check if either player has any creatures left
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()  # <-- Added proper game end
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._quit_whole_game()  # <-- Added proper game end
            return True
            
        # Force swap if active creature is fainted
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    if len(available_creatures) == 1:
                        player.active_creature = available_creatures[0]
                    else:
                        creature_choices = [SelectThing(creature) for creature in available_creatures]
                        choice = self._wait_for_choice(player, creature_choices)
                        player.active_creature = choice.thing
                    self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
                    
        return False
