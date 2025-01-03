from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.game_over = False
        
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
{self.player.display_name}'s {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
{self.bot.display_name}'s {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while not self.game_over:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self.game_over = True
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self.game_over = True
                continue
                
            # Resolve actions
            self.resolve_actions(
                (self.player, player_action),
                (self.bot, bot_action)
            )
            
            # Check for battle end
            if self.check_battle_end():
                self.game_over = True
                
        # Proper scene termination
        self._quit_whole_game()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return ("attack", self._wait_for_choice(player, choices).thing)
        else:
            valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not valid_creatures:
                return None
            choices = [SelectThing(creature) for creature in valid_creatures]
            return ("swap", self._wait_for_choice(player, choices).thing)

    def resolve_actions(self, player_data, bot_data):
        # Handle swaps first
        if player_data[1][0] == "swap":
            self.player.active_creature = player_data[1][1]
        if bot_data[1][0] == "swap":
            self.bot.active_creature = bot_data[1][1]
            
        # Then handle attacks
        first, second = self.get_action_order(player_data, bot_data)
        self.execute_action(*first)
        self.execute_action(*second)

    def get_action_order(self, player_data, bot_data):
        if player_data[1][0] == "swap" or bot_data[1][0] == "swap":
            return (player_data, bot_data)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return (player_data, bot_data)
        elif bot_speed > player_speed:
            return (bot_data, player_data)
        else:
            return random.choice([(player_data, bot_data), (bot_data, player_data)])

    def execute_action(self, actor, action):
        if action[0] != "attack":
            return
            
        skill = action[1]
        attacker = actor
        defender = self.bot if actor == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            valid_creatures = [c for c in defender.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(creature) for creature in valid_creatures]
                defender.active_creature = self._wait_for_choice(defender, choices).thing

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
