from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures HP and set initial active creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: HP {p_creature.hp}/{p_creature.max_hp}
Foe's {b_creature.display_name}: HP {b_creature.hp}/{b_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game instead of just returning

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Determine order
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first = self.bot
            second = self.player
            first_action = bot_action
            second_action = player_action
        elif self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.random() < 0.5:
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action

        # Execute actions in order
        self.execute_action(first, second, first_action)
        if second.active_creature.hp > 0:
            self.execute_action(second, first, second_action)

    def execute_action(self, attacker, defender, action):
        action_type, thing = action
        
        if action_type == "swap":
            attacker.active_creature = thing
            self._show_text(attacker, f"Swapped to {thing.display_name}!")
            
        elif action_type == "attack":
            skill = thing
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"Took {damage} damage!")
            
            if defender.active_creature.hp <= 0:
                self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
                self.handle_knockout(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_alive:
            self._show_text(self.player, "You won!")
            return True
            
        return False
