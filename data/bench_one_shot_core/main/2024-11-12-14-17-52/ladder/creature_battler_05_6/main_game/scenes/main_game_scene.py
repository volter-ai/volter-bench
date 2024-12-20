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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap (if available)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        while True:
            # First check if there are valid swap options
            valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            
            # Build choice list based on available options
            choices = [Button("Attack")]
            if valid_creatures:
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                # Show skills with Back option
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, choices)
                
                if skill_choice.display_name == "Back":
                    continue  # Go back to main choices
                return skill_choice
            else:
                # Show creatures with Back option
                choices = [SelectThing(creature) for creature in valid_creatures]
                choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, choices)
                
                if creature_choice.display_name == "Back":
                    continue  # Go back to main choices
                return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        
        # Check if first action knocked out a creature
        if self.handle_knocked_out_creature(self.player) or self.handle_knocked_out_creature(self.bot):
            return  # Skip second action if forced swap occurred
            
        self.execute_action(second)
        
        # Check again after second action
        self.handle_knocked_out_creature(self.player)
        self.handle_knocked_out_creature(self.bot)

    def handle_knocked_out_creature(self, player: Player) -> bool:
        """Forces a swap if active creature is knocked out. Returns True if swap occurred."""
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if valid_creatures:
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                choices = [SelectThing(creature) for creature in valid_creatures]
                swap_choice = self._wait_for_choice(player, choices)
                player.active_creature = swap_choice.thing
                self._show_text(player, f"Go, {player.active_creature.display_name}!")
                return True
        return False

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Skill):
            attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
            defender = self.bot if attacker == self.player else self.player
            
            damage = self.calculate_damage(action.thing, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action.thing.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            self._quit_whole_game()
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            self._quit_whole_game()
