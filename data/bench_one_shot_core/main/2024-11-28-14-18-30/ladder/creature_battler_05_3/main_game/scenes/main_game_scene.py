from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self.has_valid_swap_targets(self.player) else ""}"""

    def has_valid_swap_targets(self, player):
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Ask player if they want to play again
                play_again = Button("Play Again")
                quit_game = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again, quit_game])
                
                if choice == play_again:
                    self._transition_to_scene("MainGameScene")
                else:
                    self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            # Main action choice
            choices = [Button("Attack")]
            if self.has_valid_swap_targets(player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Skill selection with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue  # Go back to main choices
                return ("attack", choice.thing)
            else:
                # Creature selection with Back option
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                creature_choices = [SelectThing(creature) for creature in valid_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue  # Go back to main choices
                return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Swaps go first
        for player, (action_type, target) in actions:
            if action_type == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
                
        # Then attacks in speed order
        remaining_actions = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(remaining_actions) == 2:
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                ordered_actions = remaining_actions
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                ordered_actions = list(reversed(remaining_actions))
            else:
                ordered_actions = random.sample(remaining_actions, len(remaining_actions))
        else:
            ordered_actions = remaining_actions
            
        for player, (_, skill) in ordered_actions:
            defender = self.opponent if player == self.player else self.player
            self.execute_attack(player, defender, skill)

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if effectiveness > 1:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness < 1:
            self._show_text(attacker, "It's not very effective...")
            
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def handle_knockout(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature
            self._show_text(player, f"Go, {new_creature.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            winner = self.player if player_alive else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
        return False
