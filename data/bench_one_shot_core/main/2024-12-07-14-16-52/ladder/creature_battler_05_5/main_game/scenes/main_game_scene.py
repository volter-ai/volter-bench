from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize player creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        
        # Initialize bot creatures
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
        self.bot.active_creature = self.bot.creatures[0]

        # Store current turn's actions
        self.current_player_action = None
        self.current_bot_action = None

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            self.current_player_action = self.get_player_action(self.player)
            if not self.current_player_action:
                continue
                
            # Bot turn
            self.current_bot_action = self.get_bot_action()
            
            # Resolve actions
            self.resolve_actions(self.current_player_action, self.current_bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return None
            
        return ("attack", choice.thing)

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return None
            
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return None
            
        return ("swap", choice.thing)

    def get_bot_action(self):
        # Simple bot AI - randomly attack or swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return ("attack", skill)
        else:
            available_creatures = [c for c in self.bot.creatures 
                                 if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return ("swap", random.choice(available_creatures))
            return ("attack", random.choice(self.bot.active_creature.skills))

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        if self.can_continue():
            self.execute_action(second)

    def determine_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return (player_action, bot_action)
            
        p_speed = self.player.active_creature.speed
        b_speed = self.bot.active_creature.speed
        
        if p_speed > b_speed or (p_speed == b_speed and random.random() < 0.5):
            return (player_action, bot_action)
        return (bot_action, player_action)

    def execute_action(self, action):
        if action[0] != "attack":
            return
            
        skill = action[1]
        attacker = self.player if action == self.current_player_action else self.bot
        defender = self.bot if action == self.current_player_action else self.player
        
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * factor)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness.get((skill_type, creature_type), 1.0)

    def can_continue(self):
        return (self.player.active_creature.hp > 0 and 
                self.bot.active_creature.hp > 0)

    def check_battle_end(self):
        p_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        b_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not b_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        if self.player.active_creature.hp <= 0:
            self.handle_swap_choice(self.player)
        if self.bot.active_creature.hp <= 0:
            self.get_bot_action()
            
        return False
