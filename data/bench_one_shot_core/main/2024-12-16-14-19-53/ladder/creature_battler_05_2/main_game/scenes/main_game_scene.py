from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_actions = []
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.bot.display_name}'s {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP
{self.player.display_name}'s {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP

Your creatures: {', '.join(c.display_name for c in self.player.creatures if c.hp > 0)}
Opponent's creatures: {', '.join(c.display_name for c in self.bot.creatures if c.hp > 0)}"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            self.handle_player_turn(self.player)
            
            # Bot turn
            self.handle_player_turn(self.bot)
            
            # Resolve turn
            self.resolve_turn()
            
            # Check for battle end
            if self.check_battle_end():
                # After showing win/loss message, ask player what to do next
                menu_button = Button("Return to Menu")
                quit_button = Button("Quit Game")
                choice = self._wait_for_choice(self.player, [menu_button, quit_button])
                
                if choice == menu_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def handle_player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            
            choice = self._wait_for_choice(current_player, choices)
            
            if choice == attack_button:
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                
                if skill_choice == back_button:
                    continue
                
                if isinstance(skill_choice, SelectThing):
                    self.turn_actions.append(("attack", current_player, skill_choice.thing))
                    break
                    
            elif choice == swap_button:
                back_button = Button("Back")
                available_creatures = [
                    SelectThing(creature) 
                    for creature in current_player.creatures 
                    if creature.hp > 0 and creature != current_player.active_creature
                ]
                available_creatures.append(back_button)
                
                swap_choice = self._wait_for_choice(current_player, available_creatures)
                
                if swap_choice == back_button:
                    continue
                    
                if isinstance(swap_choice, SelectThing):
                    self.turn_actions.append(("swap", current_player, swap_choice.thing))
                    break

    def resolve_turn(self):
        # Handle swaps first
        for action_type, player, thing in self.turn_actions:
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(self.player, f"{player.display_name} swapped to {thing.display_name}!")

        # Then handle attacks
        attacks = [(p, t) for type_, p, t in self.turn_actions if type_ == "attack"]
        
        if len(attacks) == 2:
            # Determine order based on speed
            p1, s1 = attacks[0]
            p2, s2 = attacks[1]
            
            if p1.active_creature.speed > p2.active_creature.speed:
                order = [(p1, s1), (p2, s2)]
            elif p2.active_creature.speed > p1.active_creature.speed:
                order = [(p2, s2), (p1, s1)]
            else:
                order = random.sample(attacks, len(attacks))
                
            for attacker, skill in order:
                self.execute_attack(attacker, skill)
                
        self.turn_actions = []

    def execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.handle_fainted_creature(defender)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [
            SelectThing(creature)
            for creature in player.creatures
            if creature.hp > 0
        ]
        
        if available_creatures:
            self._show_text(self.player, f"{player.display_name} must choose a new creature!")
            choice = self._wait_for_choice(player, available_creatures)
            if isinstance(choice, SelectThing):
                player.active_creature = choice.thing
                self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
