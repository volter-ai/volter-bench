from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap (if you have other creatures available)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if player_action is None:  # No valid actions available
                self._quit_whole_game()
                return
                
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:  # No valid actions available
                self._quit_whole_game()
                return
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

            # Handle knockouts
            if not self.handle_knockouts():
                self._quit_whole_game()
                return

    def get_player_action(self, player: Player):
        choices = []
        
        # Always add Attack option if creature has skills
        if player.active_creature and player.active_creature.skills:
            choices.append(Button("Attack"))
            
        # Only add Swap if there are valid creatures to swap to
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if valid_creatures:
            choices.append(Button("Swap"))
            
        if not choices:
            return None
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player: Player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("attack", choice.thing)

    def get_swap_choice(self, player: Player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        choices = [SelectThing(creature) for creature in valid_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks based on speed
        if player_action[0] == "attack" and bot_action[0] == "attack":
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, player_action[1])
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_action[1])
            else:
                self.execute_attack(self.bot, self.player, bot_action[1])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_action[1])

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = max(1, int(raw_damage * multiplier))  # Minimum 1 damage
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False

    def handle_knockouts(self) -> bool:
        """Returns False if battle should end due to no valid swaps"""
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                valid_creatures = [c for c in player.creatures if c.hp > 0]
                if not valid_creatures:
                    return False
                    
                choices = [SelectThing(c) for c in valid_creatures]
                player.active_creature = self._wait_for_choice(player, choices).thing
                
        return True
