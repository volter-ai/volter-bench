from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill
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

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_attack_choice(self, attacker: Player) -> tuple[str, Creature, Skill]:
        skills = attacker.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        skill_choices.append(Button("Back"))
        
        choice = self._wait_for_choice(attacker, skill_choices)
        if isinstance(choice, Button):
            return None
            
        return ("attack", attacker.active_creature, choice.thing)

    def handle_swap_choice(self, player: Player) -> tuple[str, Creature, None]:
        available = self.get_available_creatures(player)
        if not available:
            self._show_text(player, "No creatures available to swap!")
            return None
            
        creature_choices = [SelectThing(creature) for creature in available]
        creature_choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, creature_choices)
        if isinstance(choice, Button):
            return None
            
        return ("swap", choice.thing, None)

    def get_player_action(self, player: Player):
        while True:
            choice = self._wait_for_choice(player, [Button("Attack"), Button("Swap")])
            
            if choice.display_name == "Attack":
                result = self.handle_attack_choice(player)
            else:
                result = self.handle_swap_choice(player)
                
            if result:
                return result

    def execute_turn(self, first_action, second_action):
        # Handle swaps first
        for action in [first_action, second_action]:
            if action and action[0] == "swap":
                player = self.player if action[1] in self.player.creatures else self.bot
                player.active_creature = action[1]
                self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")
        
        # Then handle attacks
        for action in [first_action, second_action]:
            if action and action[0] == "attack":
                attacker = self.player if action[1] in self.player.creatures else self.bot
                defender = self.bot if attacker == self.player else self.player
                
                damage = self.calculate_damage(action[1], defender.active_creature, action[2])
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(self.player, 
                    f"{action[1].display_name} used {action[2].display_name} on {defender.active_creature.display_name} for {damage} damage!")

    def force_swap(self, player: Player):
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        creature_choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")
        return True

    def run(self):
        while True:
            # Get actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Determine order
            if player_action[0] == "swap" or bot_action[0] == "swap":
                # Swaps always go first
                first = player_action if player_action[0] == "swap" else bot_action
                second = bot_action if player_action[0] == "swap" else player_action
            else:
                # Compare speeds for attacks
                player_speed = self.player.active_creature.speed
                bot_speed = self.bot.active_creature.speed
                if player_speed > bot_speed or (player_speed == bot_speed and random.random() < 0.5):
                    first, second = player_action, bot_action
                else:
                    first, second = bot_action, player_action
            
            # Execute turn
            self.execute_turn(first, second)
            
            # Check for knockouts
            if self.player.active_creature.hp <= 0:
                if not self.force_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.force_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    break
                    
        self._transition_to_scene("MainMenuScene")
