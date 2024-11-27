from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def calculate_damage(self, attacker_creature: Creature, defender_creature: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def execute_turn(self, player_action, bot_action):
        # Validate actions before executing
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if isinstance(player_action, Creature):
            self.player.active_creature = player_action
        if isinstance(bot_action, Creature):
            self.bot.active_creature = bot_action

        # Then handle attacks
        if not isinstance(player_action, Creature) and not isinstance(bot_action, Creature):
            # Determine order
            first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action

            # Execute attacks
            for attacker, defender, skill in [(first, second, first_action), (second, first, second_action)]:
                if defender.active_creature.hp > 0:  # Only attack if defender is still conscious
                    damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                    defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                    self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
                    self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted_creature(self, player: Player):
        available = self.get_available_creatures(player)
        if not available:
            return False
        
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            if choice == attack_button:
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(back_button)
                choice = self._wait_for_choice(self.player, skill_choices)
                if choice != back_button:
                    return choice.thing
            else:
                available = self.get_available_creatures(self.player)
                if available:
                    back_button = Button("Back")
                    creature_choices = [SelectThing(creature) for creature in available]
                    creature_choices.append(back_button)
                    choice = self._wait_for_choice(self.player, creature_choices)
                    if choice != back_button:
                        return choice.thing

    def get_bot_action(self):
        available = self.get_available_creatures(self.bot)
        if available and random.random() < 0.2:  # 20% chance to swap if possible
            return random.choice(available)
        return random.choice(self.bot.active_creature.skills)

    def run(self):
        while True:
            # Get actions
            player_action = self.get_player_action()
            bot_action = self.get_bot_action()

            # Execute turn
            self.execute_turn(player_action, bot_action)

            # Check for fainted creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
