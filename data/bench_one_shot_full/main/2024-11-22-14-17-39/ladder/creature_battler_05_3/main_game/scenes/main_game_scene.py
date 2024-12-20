from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

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
> Swap
> Back"""

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
                self.reset_creatures()
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button, back_button])
            
            if choice == back_button:
                return None
            
            elif choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if isinstance(skill_choice, Button):  # Back was chosen
                    continue
                return skill_choice
                
            else:  # Swap chosen
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                swap_choices.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, swap_choices)
                
                if isinstance(swap_choice, Button):  # Back was chosen
                    continue
                return swap_choice

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Then handle attacks
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for actor, action in actions:
            if isinstance(action.thing, Skill):
                self.execute_skill(actor, action.thing)
                # Check for knockouts after each attack
                if self.handle_knockouts(self.player) or self.handle_knockouts(self.opponent):
                    return

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, 
            defender.active_creature.hp - final_damage)

    def handle_knockouts(self, player) -> bool:
        """Handle knocked out creatures. Returns True if battle should end."""
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return True
            
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            swap_choices = [SelectThing(creature) for creature in available_creatures]
            swap_choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = swap_choice.thing
            
        return False

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
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost!")
            return True
        elif not has_available_creatures(self.opponent):
            self._show_text(self.player, "You won!")
            return True
            
        return False

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
