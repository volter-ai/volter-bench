from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_player(self.player)
        self.reset_player(self.bot)

    def reset_player(self, player):
        """Reset a player's creatures to full health and set initial active creature"""
        for creature in player.creatures:
            creature.hp = creature.max_hp
        player.active_creature = player.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

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
                    
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if available_creatures:
                    back_button = Button("Back")
                    swap_choice = self._wait_for_choice(player, available_creatures + [back_button])
                    
                    if swap_choice != back_button:
                        return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                self._show_text(player, f"{player.display_name} swaps to {action[1].display_name}!")
                player.active_creature = action[1]
        
        # Then handle attacks
        random.shuffle(actions)  # Randomize same-speed ties
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if action[0] == "attack":
                skill = action[1]
                attacker = player.active_creature
                defender = self.bot.active_creature if player == self.player else self.player.active_creature
                
                damage = self.calculate_damage(skill, attacker, defender)
                defender.hp = max(0, defender.hp - damage)
                
                self._show_text(player, f"{attacker.display_name} uses {skill.display_name}!")
                self._show_text(player, f"Deals {damage} damage!")
                
                if defender.hp == 0:
                    self._show_text(player, f"{defender.display_name} is knocked out!")
                    self.handle_knockout(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_knockout(self, defender):
        player = self.player if defender in self.player.creatures else self.bot
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            choices = [SelectThing(c) for c in available_creatures]
            self._show_text(player, "Choose next creature!")
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {choice.thing.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
