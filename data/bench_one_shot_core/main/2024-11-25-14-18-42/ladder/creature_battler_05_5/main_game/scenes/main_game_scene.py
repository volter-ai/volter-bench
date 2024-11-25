import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_battle()

    def _initialize_battle(self):
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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP"""

    def _get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn_choice(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self._handle_turn_choice(player)
            return ("attack", skill_choice.thing)
            
        else:
            # Show available creatures
            available = self._get_available_creatures(player)
            if not available:
                return self._handle_turn_choice(player)
                
            creature_choices = [SelectThing(creature) for creature in available]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self._handle_turn_choice(player)
            return ("swap", creature_choice.thing)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

    def _handle_forced_swap(self, player):
        available = self._get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        creature_choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def _determine_action_order(self, player_action, bot_action):
        actions = []
        
        # First handle swaps (they always go first)
        for player, action in [(self.player, player_action), (self.bot, bot_action)]:
            if action[0] == "swap":
                actions.append((player, action))
        
        # Then handle attacks based on speed
        remaining_actions = []
        for player, action in [(self.player, player_action), (self.bot, bot_action)]:
            if action[0] == "attack":
                remaining_actions.append((player, action))
                
        if len(remaining_actions) == 2:
            p1, a1 = remaining_actions[0]
            p2, a2 = remaining_actions[1]
            
            speed1 = p1.active_creature.speed
            speed2 = p2.active_creature.speed
            
            if speed1 > speed2:
                actions.extend(remaining_actions)
            elif speed2 > speed1:
                actions.extend(reversed(remaining_actions))
            else:
                # Equal speeds - random order
                if random.choice([True, False]):
                    actions.extend(remaining_actions)
                else:
                    actions.extend(reversed(remaining_actions))
        else:
            actions.extend(remaining_actions)
            
        return actions

    def run(self):
        while True:
            # Player turn choice
            player_action = self._handle_turn_choice(self.player)
            bot_action = self._handle_turn_choice(self.bot)
            
            # Determine action order and resolve
            actions = self._determine_action_order(player_action, bot_action)
            
            for player, (action_type, target) in actions:
                opponent = self.bot if player == self.player else self.player
                
                if action_type == "swap":
                    player.active_creature = target
                    self._show_text(player, f"Swapped to {target.display_name}!")
                else:  # attack
                    damage = self._calculate_damage(player.active_creature, opponent.active_creature, target)
                    opponent.active_creature.hp -= damage
                    self._show_text(player, f"{player.active_creature.display_name} used {target.display_name}!")
                    self._show_text(player, f"Dealt {damage} damage!")
                    
                    if opponent.active_creature.hp <= 0:
                        opponent.active_creature.hp = 0
                        if not self._handle_forced_swap(opponent):
                            self._show_text(self.player, 
                                "You win!" if opponent == self.bot else "You lose!")
                            self._transition_to_scene("MainMenuScene")
                            return
