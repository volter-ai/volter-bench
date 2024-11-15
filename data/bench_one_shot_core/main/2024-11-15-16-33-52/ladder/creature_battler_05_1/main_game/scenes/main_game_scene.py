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

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
            opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
            
            if not player_has_creatures:
                self._show_text(self.player, "You lost the battle!")
                self._transition_to_scene("MainMenuScene")
            elif not opponent_has_creatures:
                self._show_text(self.player, "You won the battle!")
                self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            else:  # Swap
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Resolve swaps first
        for player, action in actions:
            if action[0] == "swap":
                self._show_text(player, f"{player.active_creature.display_name} swaps out!")
                player.active_creature = action[1]
                self._show_text(player, f"{player.active_creature.display_name} swaps in!")
                
        # Then resolve attacks based on speed
        attacks = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(attacks) == 2:
            # Sort by speed
            if self.player.active_creature.speed == self.opponent.active_creature.speed:
                random.shuffle(attacks)
            else:
                attacks.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
                
        for attacker, action in attacks:
            if attacker.active_creature.hp <= 0:
                continue
                
            defender = self.opponent if attacker == self.player else self.player
            skill = action[1]
            
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp -= damage
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} uses {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} takes {damage} damage!")
            
            if defender.active_creature.hp <= 0:
                self._show_text(defender, f"{defender.active_creature.display_name} is knocked out!")
                self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def force_swap(self, player):
        available_creatures = [
            SelectThing(creature)
            for creature in player.creatures
            if creature.hp > 0 and creature != player.active_creature
        ]
        
        if available_creatures:
            self._show_text(player, "Choose a new creature!")
            choice = self._wait_for_choice(player, available_creatures)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")
