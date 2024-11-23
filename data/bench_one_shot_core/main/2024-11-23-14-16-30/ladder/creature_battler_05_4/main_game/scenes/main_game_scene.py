from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button, create_from_game_database
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
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

    def reset_creatures_state(self, player):
        """Reset all creatures to their original state using prototypes"""
        for creature in player.creatures:
            # Create fresh creature from prototype to get original stats
            fresh_creature = create_from_game_database(creature.prototype_id, type(creature))
            # Reset all battle stats
            creature.hp = fresh_creature.hp
            creature.max_hp = fresh_creature.max_hp
            creature.attack = fresh_creature.attack
            creature.defense = fresh_creature.defense
            creature.sp_attack = fresh_creature.sp_attack
            creature.sp_defense = fresh_creature.sp_defense
            creature.speed = fresh_creature.speed

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_bot_action()
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            choices = [SelectThing(c) for c in available_creatures]
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def get_bot_action(self):
        # Simple bot AI - randomly attack or swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return ("attack", skill)
        else:
            available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return ("swap", random.choice(available_creatures))
            return ("attack", random.choice(self.bot.active_creature.skills))

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")

        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        first_player = self.player if first == player_action else self.bot
        second_player = self.bot if first == player_action else self.player
        
        self.execute_action(first, first_player, second_player)
        
        # Only execute second action if defender's creature still alive
        if second_player.active_creature.hp > 0:
            self.execute_action(second, second_player, first_player)

    def get_action_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return (player_action, bot_action) if player_action[0] == "swap" else (bot_action, player_action)
            
        p_speed = self.player.active_creature.speed
        b_speed = self.bot.active_creature.speed
        
        if p_speed > b_speed or (p_speed == b_speed and random.random() < 0.5):
            return (player_action, bot_action)
        return (bot_action, player_action)

    def execute_action(self, action, attacker, defender):
        if action[0] == "attack":
            skill = action[1]
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, 
                f"{'You' if attacker == self.player else 'Foe'} used {skill.display_name}! Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            self._show_text(self.player, "You win!" if p_alive else "You lose!")
            # Reset creature states before ending
            self.reset_creatures_state(self.player)
            self.reset_creatures_state(self.bot)
            self._quit_whole_game()
            
        if self.player.active_creature.hp == 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                choice = self._wait_for_choice(self.player, 
                    [SelectThing(c) for c in available])
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp == 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self.bot.active_creature = random.choice(available)
