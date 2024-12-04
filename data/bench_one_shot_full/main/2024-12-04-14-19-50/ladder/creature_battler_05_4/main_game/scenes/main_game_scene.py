from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.type_effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5},
            "normal": {}
        }

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        effectiveness = self.type_effectiveness.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        return int(raw_damage * effectiveness)

    def execute_turn(self, player_action, bot_action):
        # Determine order
        first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
        second = self.bot if first == self.player else self.player
        first_action = player_action if first == self.player else bot_action
        second_action = bot_action if first == self.player else player_action

        # Handle swaps first
        if isinstance(first_action, Creature):
            first.active_creature = first_action
        if isinstance(second_action, Creature):
            second.active_creature = second_action

        # Execute attacks
        if isinstance(first_action, Skill):
            damage = self.calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp = max(0, second.active_creature.hp - damage)
            self._show_text(first, f"{first.active_creature.display_name} used {first_action.display_name}!")
            self._show_text(second, f"{first.active_creature.display_name} used {first_action.display_name}!")

        if isinstance(second_action, Skill) and second.active_creature.hp > 0:
            damage = self.calculate_damage(second.active_creature, first.active_creature, second_action)
            first.active_creature.hp = max(0, first.active_creature.hp - damage)
            self._show_text(first, f"{second.active_creature.display_name} used {second_action.display_name}!")
            self._show_text(second, f"{second.active_creature.display_name} used {second_action.display_name}!")

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def force_swap(self, player: Player) -> bool:
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        # Initialize battle
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature stats
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            player_action = None
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                player_action = self._wait_for_choice(self.player, skill_choices).thing
            else:
                available = self.get_available_creatures(self.player)
                if available:
                    creature_choices = [SelectThing(c) for c in available]
                    player_action = self._wait_for_choice(self.player, creature_choices).thing

            # Bot turn
            bot_action = None
            if random.random() < 0.8:  # 80% chance to attack
                bot_action = random.choice(self.bot.active_creature.skills)
            else:
                available = self.get_available_creatures(self.bot)
                if available:
                    bot_action = random.choice(available)

            # Execute turn
            self.execute_turn(player_action, bot_action)

            # Check for knockouts and force swaps
            if self.player.active_creature.hp <= 0:
                if not self.force_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    # Reset creatures before leaving
                    for creature in self.player.creatures + self.bot.creatures:
                        creature.hp = creature.max_hp
                    self._quit_whole_game()  # Properly end the game
                    return

            if self.bot.active_creature.hp <= 0:
                if not self.force_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    # Reset creatures before leaving
                    for creature in self.player.creatures + self.bot.creatures:
                        creature.hp = creature.max_hp
                    self._quit_whole_game()  # Properly end the game
                    return
