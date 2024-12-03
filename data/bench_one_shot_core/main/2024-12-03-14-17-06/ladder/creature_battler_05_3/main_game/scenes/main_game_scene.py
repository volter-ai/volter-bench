from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

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
> Swap (if you have other creatures available)"""

    def run(self):
        while True:
            # Check if active creatures are knocked out and force swaps
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()  # Fixed: Call quit_whole_game instead of breaking
            
            if self.opponent.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.opponent):
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()  # Fixed: Call quit_whole_game instead of breaking

            # Get actions
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_forced_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player):
        # Build choice list based on available options
        choices = [Button("Attack")]
        
        # Only add swap if there are creatures to swap to
        available_creatures = self.get_available_creatures(player)
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Then handle attacks
        if self.player.active_creature.speed >= self.opponent.active_creature.speed:
            self.execute_skill(player_action, self.player, self.opponent)
            self.execute_skill(opponent_action, self.opponent, self.player)
        else:
            self.execute_skill(opponent_action, self.opponent, self.player)
            self.execute_skill(player_action, self.player, self.opponent)

    def execute_skill(self, action, attacker, defender):
        if isinstance(action.thing, Creature):
            return
            
        skill = action.thing
        attacker_creature = attacker.active_creature
        defender_creature = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
