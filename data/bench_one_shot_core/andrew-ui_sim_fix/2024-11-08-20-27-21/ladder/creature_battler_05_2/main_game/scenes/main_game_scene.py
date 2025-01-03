from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, BotListener
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

    def get_player_action(self, player: Player) -> tuple[bool, any]:
        """Gets a valid action for the given player, returns (has_action, action)"""
        # Check if player can make any moves
        if player.active_creature.hp <= 0:
            if not self.handle_fainted(player):
                return False, None
            return True, None

        if isinstance(player._listener, BotListener):
            # Bot logic
            available_creatures = self.get_available_creatures(player)
            
            # Decide whether to attack or swap
            if random.random() < 0.8 and player.active_creature.skills:  # 80% chance to attack if possible
                return True, random.choice(player.active_creature.skills)
            elif available_creatures:  # Try to swap if we can't/don't attack
                return True, random.choice(available_creatures)
            elif player.active_creature.skills:  # Fall back to attack if we can't swap
                return True, random.choice(player.active_creature.skills)
            return False, None  # No valid moves
            
        else:
            # Human logic - now with Back functionality
            while True:
                attack = Button("Attack")
                swap = Button("Swap")
                choice = self._wait_for_choice(player, [attack, swap])
                
                if choice == attack and player.active_creature.skills:
                    back = Button("Back")
                    choices = [SelectThing(s) for s in player.active_creature.skills]
                    choices.append(back)
                    choice = self._wait_for_choice(player, choices)
                    if choice == back:
                        continue
                    return True, choice.thing
                elif choice == swap:
                    available = self.get_available_creatures(player)
                    if available:
                        back = Button("Back")
                        choices = [SelectThing(c) for c in available]
                        choices.append(back)
                        choice = self._wait_for_choice(player, choices)
                        if choice == back:
                            continue
                        return True, choice.thing
                return False, None

    def execute_turn(self, first_player, first_action, second_player, second_action):
        # Handle swaps first
        for player, action in [(first_player, first_action), (second_player, second_action)]:
            if action and isinstance(action, Creature):
                player.active_creature = action
                self._show_text(self.player, f"{player.display_name} swapped to {action.display_name}!")

        # Then handle attacks
        for player, opponent, action in [(first_player, second_player, first_action), 
                                       (second_player, first_player, second_action)]:
            if not action or isinstance(action, Creature):
                continue
                
            if player.active_creature.hp <= 0:
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
            # Get actions for both players
            has_player_action, player_action = self.get_player_action(self.player)
            has_bot_action, bot_action = self.get_player_action(self.bot)

            # If neither player can act, something is wrong
            if not has_player_action and not has_bot_action:
                self._show_text(self.player, "Battle ended in a draw - no valid moves!")
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
