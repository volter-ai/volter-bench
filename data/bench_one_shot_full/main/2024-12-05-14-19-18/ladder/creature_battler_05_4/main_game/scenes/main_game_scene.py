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
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

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
            battle_result = self.check_battle_end()
            if battle_result:
                self._show_text(self.player, battle_result)
                self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            # Main action menu
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
                    return None
                    
                back_button = Button("Back")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue
                return creature_choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, opponent_action)
        self.execute_action(first)
        self.execute_action(second)

    def get_action_order(self, player_action, opponent_action):
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return player_action, opponent_action
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            return opponent_action, player_action
        else:
            return random.choice([(player_action, opponent_action), (opponent_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Skill):
            attacker = self.player if action.thing in self.player.active_creature.skills else self.opponent
            defender = self.opponent if attacker == self.player else self.player
            
            damage = self.calculate_damage(action.thing, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action.thing.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, skill, attacker, defender):
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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            return "You lost!"
        elif not opponent_has_creatures:
            return "You won!"
            
        return None

    def _transition_to_scene(self, scene_name: str):
        # Reset creature states before leaving
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        # Call parent implementation to do the actual transition
        super()._transition_to_scene(scene_name)
