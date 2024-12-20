from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}"""

    def _format_team(self, player: Player) -> str:
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                continue
                
            # Resolution phase
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _handle_turn(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player: Player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return None
        
        return ("attack", choice.thing)

    def _handle_swap(self, player: Player):
        available_creatures = [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return None
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return None
            
        return ("swap", choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        first, second = self._determine_order(player_action, bot_action)
        first_is_player = first == player_action
        second_is_player = second == player_action
        
        self._execute_action(first, is_player_action=first_is_player)
        self._execute_action(second, is_player_action=second_is_player)

    def _determine_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return player_action, bot_action
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def _execute_action(self, action, is_player_action: bool):
        if action[0] == "attack":
            attacker = self.player if is_player_action else self.bot
            defender = self.bot if is_player_action else self.player
            
            skill = action[1]
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"Dealt {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        if self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        if self.bot.active_creature.hp == 0:
            self._force_swap(self.bot)
            
        return False

    def _force_swap(self, player: Player):
        available = [c for c in player.creatures if c.hp > 0]
        if available:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
