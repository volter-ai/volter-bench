from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.cleanup()
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(back_button)
                
                subchoice = self._wait_for_choice(player, choices)
                if subchoice == back_button:
                    continue
                return subchoice
            else:
                available_creatures = [c for c in player.creatures 
                                     if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                choices = [SelectThing(creature) for creature in available_creatures]
                choices.append(back_button)
                
                subchoice = self._wait_for_choice(player, choices)
                if subchoice == back_button:
                    continue
                return subchoice

    def force_swap_if_needed(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return False
                
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player,
                [SelectThing(creature) for creature in available_creatures])
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")
            return True
        return True

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Determine order for attacks
        first = self.player
        second = self.opponent
        first_action = player_action
        second_action = opponent_action
        
        if (isinstance(player_action.thing, Skill) and 
            isinstance(opponent_action.thing, Skill)):
            if (self.opponent.active_creature.speed > 
                self.player.active_creature.speed):
                first = self.opponent
                second = self.player
                first_action = opponent_action
                second_action = player_action
            elif (self.opponent.active_creature.speed == 
                  self.player.active_creature.speed):
                if random.random() < 0.5:
                    first = self.opponent
                    second = self.player
                    first_action = opponent_action
                    second_action = player_action
                    
        # Execute attacks and handle knockouts
        if isinstance(first_action.thing, Skill):
            self.execute_attack(first, second, first_action.thing)
            if not self.force_swap_if_needed(second):
                return
                
        if isinstance(second_action.thing, Skill):
            self.execute_attack(second, first, second_action.thing)
            if not self.force_swap_if_needed(first):
                return

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, 
            defender.active_creature.hp - final_damage)
            
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"It dealt {final_damage} damage!")

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
        def check_player_loss(player):
            return all(c.hp <= 0 for c in player.creatures)
            
        if check_player_loss(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif check_player_loss(self.opponent):
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False

    def cleanup(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
