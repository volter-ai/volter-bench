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
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_turn_choice(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                available = self.get_available_creatures(player)
                if not available:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available]
                creature_choices.append(back_button)
                creature_choice = self._wait_for_choice(player, creature_choices)
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def execute_turn(self, p1_action, p2_action):
        # Handle swaps first
        if p1_action[0] == "swap":
            self.player.active_creature = p1_action[1]
        if p2_action[0] == "swap":
            self.bot.active_creature = p2_action[1]

        # Then handle attacks
        if p1_action[0] == "attack" and p2_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, p1_action[1]), (self.bot, p2_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, p2_action[1]), (self.player, p1_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, p1_action[1]), (self.bot, p2_action[1])
                else:
                    first, second = (self.bot, p2_action[1]), (self.player, p1_action[1])

            # Execute attacks in order
            for attacker, skill in [first, second]:
                if attacker == self.player:
                    defender = self.bot
                else:
                    defender = self.player
                    
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_fainted(self, player: Player):
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return True
                
            self._show_text(player, f"{player.active_creature.display_name} fainted!")
            if player == self.player:
                creature_choices = [SelectThing(creature) for creature in available]
                choice = self._wait_for_choice(player, creature_choices)
                player.active_creature = choice.thing
            else:
                player.active_creature = available[0]
                
        return False

    def run(self):
        while True:
            # Player turn choice
            p1_action = self.handle_turn_choice(self.player)
            
            # Bot turn choice 
            p2_action = self.handle_turn_choice(self.bot)
            
            # Execute turn
            self.execute_turn(p1_action, p2_action)
            
            # Check for fainted creatures
            player_lost = self.check_fainted(self.player)
            bot_lost = self.check_fainted(self.bot)
            
            if player_lost:
                self._show_text(self.player, "You lost!")
                break
            elif bot_lost:
                self._show_text(self.player, "You won!")
                break
                
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
