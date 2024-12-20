from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from main_game.models import Creature

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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}

> Attack
> Swap"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._get_player_action(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _get_player_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])

            if choice == attack:
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice == back:
                    continue
                return ("attack", skill_choice, player.active_creature)  # Store the creature that queued this attack
                
            elif choice == swap:
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                swap_choices = [SelectThing(c) for c in available_creatures]
                back = Button("Back")
                swap_choice = self._wait_for_choice(player, swap_choices + [back])
                if swap_choice == back:
                    continue
                return ("swap", swap_choice.thing, None)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks based on speed
        if player_action[0] == "attack" and bot_action[0] == "attack":
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            # Determine order based on speed, with random resolution for ties
            if player_speed > bot_speed:
                first, second = (self.player, player_action[1], player_action[2]), (self.bot, bot_action[1], bot_action[2])
            elif bot_speed > player_speed:
                first, second = (self.bot, bot_action[1], bot_action[2]), (self.player, player_action[1], player_action[2])
            else:
                # Equal speeds - randomly determine order
                actors = [(self.player, player_action[1], player_action[2]), (self.bot, bot_action[1], bot_action[2])]
                random.shuffle(actors)
                first, second = actors
            
            # Execute first attack
            self._execute_attack(first[0], self.bot if first[0] == self.player else self.player, first[1])
            
            # Handle any necessary swaps after first attack
            if self._handle_knockouts():
                return  # Battle ended during swaps
                
            # Only execute second attack if the original creature that queued it is still active
            attacker = second[0]
            defender = self.bot if attacker == self.player else self.player
            original_creature = second[2]
            
            if attacker.active_creature == original_creature:
                self._execute_attack(attacker, defender, second[1])
                self._handle_knockouts()

    def _execute_attack(self, attacker, defender, skill_button):
        skill = next(s for s in attacker.active_creature.skills if s.display_name == skill_button.display_name)
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def _handle_knockouts(self):
        """Handle any knocked out creatures, returns True if battle should end"""
        for player in [self.player, self.bot]:
            if player.active_creature.hp == 0:
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if not available_creatures:
                    winner = self.bot if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    return True
                    
                swap_choices = [SelectThing(c) for c in available_creatures]
                swap_choice = self._wait_for_choice(player, swap_choices)
                player.active_creature = swap_choice.thing
        
        return False

    def _get_type_multiplier(self, skill_type, creature_type):
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

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
            
        return False
