from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_battle()

    def _initialize_battle(self):
        # Reset creatures
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
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def _calculate_damage(self, attacker_creature: Creature, defender_creature: Creature, skill: Skill):
        # Calculate type effectiveness
        type_effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                type_effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                type_effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                type_effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                type_effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                type_effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                type_effectiveness = 0.5

        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        return int(raw_damage * type_effectiveness)

    def _execute_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action, Creature):
            self.player.active_creature = player_action
        if isinstance(bot_action, Creature):
            self.bot.active_creature = bot_action

        # Only handle attacks if both actions are skills
        if isinstance(player_action, Skill) and isinstance(bot_action, Skill):
            first = self.player
            second = self.bot
            first_action = player_action
            second_action = bot_action
            
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and random.random() < 0.5):
                first, second = second, first
                first_action, second_action = second_action, first_action

            # Execute attacks
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp -= damage
            self._show_text(self.player, f"{first.active_creature.display_name} used {first_action.display_name}!")
            self._show_text(self.player, f"Dealt {damage} damage!")

            if second.active_creature.hp > 0:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_action)
                first.active_creature.hp -= damage
                self._show_text(self.player, f"{second.active_creature.display_name} used {second_action.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")

    def _handle_knockouts(self, player: Player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return False
            
            choices = [SelectThing(c) for c in available_creatures]
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def run(self):
        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            player_action = None
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                player_action = skill_choice.thing
            else:
                available_creatures = [c for c in self.player.creatures if c.hp > 0 and c != self.player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    player_action = creature_choice.thing
                else:
                    # If no valid swap targets, force an attack
                    skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                    skill_choice = self._wait_for_choice(self.player, skill_choices)
                    player_action = skill_choice.thing

            # Bot turn - ensure bot always makes a valid choice
            if random.random() < 0.2 and len([c for c in self.bot.creatures if c.hp > 0 and c != self.bot.active_creature]) > 0:
                available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != self.bot.active_creature]
                bot_action = random.choice(available_creatures)
            else:
                bot_action = random.choice(self.bot.active_creature.skills)

            # Execute turn only if both actions are valid
            if player_action and bot_action:
                self._execute_turn(player_action, bot_action)

            # Handle knockouts
            if not self._handle_knockouts(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self._handle_knockouts(self.bot):
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
