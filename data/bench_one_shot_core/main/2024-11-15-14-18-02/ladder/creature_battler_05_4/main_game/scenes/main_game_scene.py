from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset both players' creatures
        self._reset_player_creatures(self.player)
        self._reset_player_creatures(self.bot)
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _reset_player_creatures(self, player):
        """Helper method to reset all creatures' HP to their max values"""
        for creature in player.creatures:
            creature.hp = creature.max_hp
        player.active_creature = None

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        status = f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your other creatures:"""
        
        for c in self.player.creatures:
            if c != player_creature:
                status += f"\n- {c.display_name}: HP {c.hp}/{c.max_hp}"
                
        return status

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                # Player has no creatures left
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                # Bot has no creatures left
                self._show_text(self.player, "You won the battle!")
                self._quit_whole_game()
                return
                
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                if any(c.hp > 0 for c in self.player.creatures):
                    self._show_text(self.player, "You won the battle!")
                else:
                    self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
                return

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, f"{player.display_name} has no creatures left!")
                return None
                
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
            player.active_creature = choice.thing
            return ("swap", choice.thing)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            skill_choice = self._wait_for_choice(player, 
                [Button(s.display_name) for s in player.active_creature.skills])
            return ("attack", next(s for s in player.active_creature.skills 
                if s.display_name == skill_choice.display_name))
        else:
            available_creatures = [c for c in player.creatures 
                if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                return self.get_player_action(player)
                
            choice = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
            player.active_creature = choice.thing
            return ("swap", choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
        if bot_action[0] == "swap":
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)
            
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, skill)

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + skill.base_damage 
                - defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense 
                * skill.base_damage)
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, 
            defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
            
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness_text}")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        return not player_has_creatures or not bot_has_creatures
