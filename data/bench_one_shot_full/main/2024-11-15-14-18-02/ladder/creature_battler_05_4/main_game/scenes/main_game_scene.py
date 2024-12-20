from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

Your Team:
{self.format_team(self.player)}

Opponent's Team:
{self.format_team(self.opponent)}

> Attack
> Swap"""

    def format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

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
            
            # Handle knocked out creatures
            if self.handle_knockouts():
                self.cleanup()
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue
                return skill_choice
            else:
                # Show available creatures with Back option
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                
                back_button = Button("Back")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue
                return creature_choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
            
        if isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            self.opponent.active_creature = opponent_action.thing

        # Then handle attacks
        first, second = self.get_action_order(player_action, opponent_action)
        self.execute_action(first)
        if not self.handle_knockouts():  # Check knockouts between actions
            self.execute_action(second)
            self.handle_knockouts()

    def handle_knockouts(self):
        """Handle knocked out creatures and force swaps. Returns True if battle should end."""
        for player in [self.player, self.opponent]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if not available_creatures:
                    winner = self.opponent if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    return True
                
                self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                swap_choice = self._wait_for_choice(player, swap_choices)
                player.active_creature = swap_choice.thing
                
        return False

    def get_action_order(self, player_action, opponent_action):
        # Swaps always go first
        if isinstance(player_action.thing, type(self.player.creatures[0])) or \
           isinstance(opponent_action.thing, type(self.opponent.creatures[0])):
            return (player_action, opponent_action)
            
        p_speed = self.player.active_creature.speed
        o_speed = self.opponent.active_creature.speed
        
        if p_speed > o_speed or (p_speed == o_speed and random.random() < 0.5):
            return (player_action, opponent_action)
        return (opponent_action, player_action)

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return  # Swap already handled
            
        skill = action.thing
        attacker = self.player.active_creature if action == self.player else self.opponent.active_creature
        defender = self.opponent.active_creature if action == self.player else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def cleanup(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
