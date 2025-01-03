from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Actions:
> Attack
> Swap"""

    def run(self):
        while True:
            # Player phase
            player_action = None
            while player_action is None:  # Keep prompting until valid action selected
                player_action = self.get_player_action(self.player)
            
            # Bot phase
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._quit_whole_game()
                return
                
            # Resolution phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills with Back option
            back_button = Button("Back")
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None  # Return to main menu
            return choice
            
        else:  # Swap selected
            # Show available creatures with Back option
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                return None
                
            back_button = Button("Back")
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None  # Return to main menu
            return choice

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Determine attack order
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            first, second = self.player, self.bot
            first_action, second_action = player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            first, second = self.bot, self.player
            first_action, second_action = bot_action, player_action
        else:
            if random.random() < 0.5:
                first, second = self.player, self.bot
                first_action, second_action = player_action, bot_action
            else:
                first, second = self.bot, self.player
                first_action, second_action = bot_action, player_action

        # Execute attacks
        if isinstance(first_action.thing, Skill):
            self.execute_attack(first, second, first_action.thing)
        if isinstance(second_action.thing, Skill) and second.active_creature.hp > 0:
            self.execute_attack(second, first, second_action.thing)

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
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
