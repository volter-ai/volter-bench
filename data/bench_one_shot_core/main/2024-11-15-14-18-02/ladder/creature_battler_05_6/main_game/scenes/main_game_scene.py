import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset all creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Determine order for attacks
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if (self.bot.active_creature.speed > self.player.active_creature.speed or 
            (self.bot.active_creature.speed == self.player.active_creature.speed and 
             random.random() < 0.5)):
            first, second = second, first
            first_action, second_action = second_action, first_action

        # Execute attacks
        if first_action[0] == "attack":
            self.execute_attack(first, second, first_action[1])
        if second.active_creature.hp > 0 and second_action[0] == "attack":
            self.execute_attack(second, first, second_action[1])

        # Force swaps for fainted creatures
        self.handle_fainted_creatures()

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, 
                       f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creatures(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available_creatures = [
                    SelectThing(c) for c in player.creatures if c.hp > 0
                ]
                if available_creatures:
                    self._show_text(player, f"{player.active_creature.display_name} fainted!")
                    swap_choice = self._wait_for_choice(player, available_creatures)
                    player.active_creature = swap_choice.thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)

        if not player_has_creatures or not bot_has_creatures:
            winner = self.player if player_has_creatures else self.bot
            self._show_text(self.player, 
                          "You win!" if winner == self.player else "You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
