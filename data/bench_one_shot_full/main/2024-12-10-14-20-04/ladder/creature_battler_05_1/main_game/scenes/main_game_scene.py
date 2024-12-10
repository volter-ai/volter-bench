from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
> Swap
"""

    def run(self):
        while True:
            # Player phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Bot phase
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            # Resolution phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player: Player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return self.get_player_action(player)
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            
        # Then handle attacks
        first, second = self.determine_turn_order(player_action, bot_action)
        self.execute_action(first[0], first[1])
        if second[1].active_creature.hp > 0:  # Only execute second action if target still alive
            self.execute_action(second[0], second[1])

    def determine_turn_order(self, player_action, bot_action):
        if player_action["type"] == "swap" or bot_action["type"] == "swap":
            return (player_action, self.bot), (bot_action, self.player)
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (player_action, self.bot), (bot_action, self.player)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return (bot_action, self.player), (player_action, self.bot)
        else:
            if random.random() < 0.5:
                return (player_action, self.bot), (bot_action, self.player)
            return (bot_action, self.player), (player_action, self.bot)

    def execute_action(self, action, target: Player):
        if action["type"] == "attack":
            skill = action["skill"]
            damage = self.calculate_damage(skill, target.active_creature)
            target.active_creature.hp = max(0, target.active_creature.hp - damage)
            
            if target.active_creature.hp == 0:
                self.handle_fainted_creature(target)

    def calculate_damage(self, skill, target_creature: Creature):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = skill.base_damage + self.player.active_creature.attack - target_creature.defense
        else:
            raw_damage = (skill.base_damage * self.player.active_creature.sp_attack) / target_creature.sp_defense
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target_creature.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            winner = self.player if player == self.bot else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = self.player if bot_has_creatures else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
