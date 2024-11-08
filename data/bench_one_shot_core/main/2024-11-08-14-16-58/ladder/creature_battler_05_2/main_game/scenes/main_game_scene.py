from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = player.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted(self, player: Player):
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player: Player):
        while True:
            # Get valid actions for main menu
            can_attack = player.active_creature and player.active_creature.hp > 0
            can_swap = bool(self.get_available_creatures(player))
            
            if not (can_attack or can_swap):
                return None
                
            choices = []
            if can_attack:
                choices.append(Button("Attack"))
            if can_swap:
                choices.append(Button("Swap"))
                
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                choices = [SelectThing(s) for s in player.active_creature.skills]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(player, choices)
                
                if isinstance(choice, Button) and choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice.thing
            else:
                # Swap submenu
                choices = [SelectThing(c) for c in self.get_available_creatures(player)]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(player, choices)
                
                if isinstance(choice, Button) and choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice.thing

    def get_bot_action(self):
        # Get valid actions
        can_attack = self.bot.active_creature and self.bot.active_creature.hp > 0
        available_creatures = self.get_available_creatures(self.bot)
        
        if not (can_attack or available_creatures):
            return None
            
        if can_attack and (random.random() < 0.8 or not available_creatures):
            return random.choice(self.bot.active_creature.skills)
        elif available_creatures:
            return random.choice(available_creatures)
        return None

    def execute_turn(self, first_player, first_action, second_player, second_action):
        # Handle swaps first
        for player, action in [(first_player, first_action), (second_player, second_action)]:
            if isinstance(action, Creature):
                player.active_creature = action
                self._show_text(self.player, f"{player.display_name} swapped to {action.display_name}!")

        # Then handle attacks
        for player, opponent, action in [(first_player, second_player, first_action), 
                                       (second_player, first_player, second_action)]:
            if not action or isinstance(action, Creature):
                continue
                
            damage = self.calculate_damage(player.active_creature, opponent.active_creature, action)
            opponent.active_creature.hp = max(0, opponent.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{player.display_name}'s {player.active_creature.display_name} used {action.display_name}!")
            self._show_text(self.player,
                f"{opponent.active_creature.display_name} took {damage} damage!")
            
            if opponent.active_creature.hp == 0:
                self._show_text(self.player,
                    f"{opponent.active_creature.display_name} fainted!")
                if not self.handle_fainted(opponent):
                    self._show_text(self.player,
                        f"{opponent.display_name} has no creatures left!")
                    return opponent
        return None

    def run(self):
        while True:
            # Get actions
            player_action = self.get_player_action(self.player)
            if player_action is None:
                self._show_text(self.player, "You have no valid moves left!")
                self._show_text(self.player, "You lose!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
                
            bot_action = self.get_bot_action()
            if bot_action is None:
                self._show_text(self.player, "Opponent has no valid moves left!")
                self._show_text(self.player, "You win!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            # Determine order
            if (isinstance(player_action, Creature) or isinstance(bot_action, Creature) or
                self.player.active_creature.speed > self.bot.active_creature.speed or
                (self.player.active_creature.speed == self.bot.active_creature.speed and 
                 random.random() < 0.5)):
                first = (self.player, player_action)
                second = (self.bot, bot_action)
            else:
                first = (self.bot, bot_action)
                second = (self.player, player_action)

            loser = self.execute_turn(first[0], first[1], second[0], second[1])
            
            if loser:
                self._show_text(self.player,
                    "You win!" if loser == self.bot else "You lose!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
