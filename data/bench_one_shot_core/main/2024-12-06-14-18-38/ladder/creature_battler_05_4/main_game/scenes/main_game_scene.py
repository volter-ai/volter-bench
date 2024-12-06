from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal" or defender_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_turn(self, player: Player, opponent: Player):
        while True:  # Allow returning to main menu with Back option
            # Main menu
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue  # Return to main menu
                return ("attack", skill_choice.thing)
            else:
                # Show available creatures with Back option
                available = self.get_available_creatures(player)
                if not available:
                    return None
                    
                creature_choices = [SelectThing(creature) for creature in available]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue  # Return to main menu
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player turn
            player_action = self.handle_turn(self.player, self.bot)
            if not player_action:
                self._show_text(self.player, "You have no more creatures!")
                break

            # Bot turn
            bot_action = self.handle_turn(self.bot, self.player)
            if not bot_action:
                self._show_text(self.player, "Opponent has no more creatures!")
                break

            # Resolution phase
            self.resolve_actions(self.player, self.bot, player_action, bot_action)

            # Check for battle end
            if all(c.hp <= 0 for c in self.player.creatures):
                self._show_text(self.player, "You lost!")
                break
            elif all(c.hp <= 0 for c in self.bot.creatures):
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def resolve_actions(self, player: Player, bot: Player, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            bot.active_creature = bot_action[1]

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order
            if player.active_creature.speed > bot.active_creature.speed:
                first, second = (player, player_action[1]), (bot, bot_action[1])
            elif player.active_creature.speed < bot.active_creature.speed:
                first, second = (bot, bot_action[1]), (player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (player, player_action[1]), (bot, bot_action[1])
                else:
                    first, second = (bot, bot_action[1]), (player, player_action[1])

            # Execute attacks
            for attacker, skill in [first, second]:
                if attacker == player:
                    defender = bot
                else:
                    defender = player
                    
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

                # Force swap if creature fainted
                if defender.active_creature.hp <= 0:
                    available = self.get_available_creatures(defender)
                    if available:
                        if defender == player:
                            creature_choices = [SelectThing(creature) for creature in available]
                            new_creature = self._wait_for_choice(defender, creature_choices).thing
                            defender.active_creature = new_creature
                        else:
                            defender.active_creature = available[0]
