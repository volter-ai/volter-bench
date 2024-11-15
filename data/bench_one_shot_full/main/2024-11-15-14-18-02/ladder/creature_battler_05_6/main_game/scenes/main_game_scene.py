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
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue

            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            
            skill_choice = self._wait_for_choice(player, skill_choices)
            if skill_choice == back_button:
                return None
                
            return ("attack", skill_choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(back_button)
            
            creature_choice = self._wait_for_choice(player, creature_choices)
            if creature_choice == back_button:
                return None
                
            return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]

        # Determine action order based on speed
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            first, second = (self.player, player_action), (self.opponent, opponent_action)
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            first, second = (self.opponent, opponent_action), (self.player, player_action)
        else:
            if random.random() < 0.5:
                first, second = (self.player, player_action), (self.opponent, opponent_action)
            else:
                first, second = (self.opponent, opponent_action), (self.player, player_action)

        # Execute actions
        for attacker, action in [first, second]:
            if action[0] == "attack":
                self.execute_attack(attacker, action[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.opponent
        else:
            defender = self.player

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)

        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

        # Handle fainted creature
        if defender.active_creature.hp == 0:
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
