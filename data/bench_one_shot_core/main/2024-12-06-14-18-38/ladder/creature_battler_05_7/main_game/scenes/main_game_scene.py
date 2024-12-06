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
        while True:  # Allow returning to main menu with Back button
            # Main menu choices
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue  # Go back to main menu
                return ("attack", skill_choice.thing)
                
            else:  # Swap chosen
                # Show available creatures with Back option
                available = self.get_available_creatures(player)
                if not available:
                    return None
                    
                back_button = Button("Back")
                creature_choices = [SelectThing(creature) for creature in available]
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue  # Go back to main menu
                return ("swap", creature_choice.thing)

    def handle_battle_end(self, winner: Player, loser: Player):
        if winner == self.player:
            self._show_text(self.player, "Congratulations! You have won the battle!")
        else:
            self._show_text(self.player, "Game Over! You have been defeated!")
        self._quit_whole_game()

    def resolve_speed_order(self, attack_actions):
        # Group actions by speed
        speed_groups = {}
        for action in attack_actions:
            speed = action[0].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)
        
        # Build final order, randomly ordering within same speed
        ordered_actions = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            actions = speed_groups[speed]
            if len(actions) > 1:
                # Randomly shuffle actions with same speed
                random.shuffle(actions)
            ordered_actions.extend(actions)
            
        return ordered_actions

    def run(self):
        while True:
            # Player turn
            player_action = self.handle_turn(self.player, self.bot)
            if not player_action:
                self._show_text(self.player, "You have no more creatures!")
                self.handle_battle_end(winner=self.bot, loser=self.player)
                
            # Bot turn
            bot_action = self.handle_turn(self.bot, self.player)
            if not bot_action:
                self._show_text(self.player, "You won! The opponent has no more creatures!")
                self.handle_battle_end(winner=self.player, loser=self.bot)

            # Resolve actions
            actions = [(self.player, player_action), (self.bot, bot_action)]
            
            # Handle swaps first
            for player, action in actions:
                if action[0] == "swap":
                    player.active_creature = action[1]
                    self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")

            # Then handle attacks with proper speed ordering
            attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
            ordered_attacks = self.resolve_speed_order(attack_actions)
            
            for attacker, action in ordered_attacks:
                if attacker.active_creature.hp <= 0:
                    continue
                    
                defender = self.bot if attacker == self.player else self.player
                skill = action[1]
                
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")
                
                if defender.active_creature.hp <= 0:
                    self._show_text(self.player, 
                        f"{defender.active_creature.display_name} was knocked out!")
                    
                    available = self.get_available_creatures(defender)
                    if not available:
                        if defender == self.player:
                            self.handle_battle_end(winner=self.bot, loser=self.player)
                        else:
                            self.handle_battle_end(winner=self.player, loser=self.bot)
                    
                    creature_choices = [SelectThing(creature) for creature in available]
                    new_creature = self._wait_for_choice(defender, creature_choices).thing
                    defender.active_creature = new_creature
                    self._show_text(self.player,
                        f"{defender.display_name} sent out {new_creature.display_name}!")
