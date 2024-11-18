from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creature HP at start of battle
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

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
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}

            else: # Swap
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                creature_choice = self._wait_for_choice(player, available_creatures)
                
                if isinstance(creature_choice, Button):
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # First handle all swaps
        swap_actions = []
        attack_actions = []
        
        for player, action in [(self.player, player_action), (self.bot, bot_action)]:
            if action["type"] == "swap":
                swap_actions.append((player, action))
            else:
                attack_actions.append((player, action))
                
        # Execute swaps first
        for player, action in swap_actions:
            old_creature = player.active_creature
            player.active_creature = action["creature"]
            self._show_text(self.player, f"{player.display_name} swapped {old_creature.display_name} for {action['creature'].display_name}!")
            
        # Then handle attacks based on speed
        if len(attack_actions) == 2:
            # Both players attacked - determine order by speed
            player1, action1 = attack_actions[0]
            player2, action2 = attack_actions[1]
            
            speed1 = player1.active_creature.speed
            speed2 = player2.active_creature.speed
            
            # If speeds are equal, randomize order
            if speed1 == speed2:
                if random.random() < 0.5:
                    attack_actions = [attack_actions[1], attack_actions[0]]
            # Otherwise, sort by speed (higher speed goes first)
            elif speed1 < speed2:
                attack_actions = [attack_actions[1], attack_actions[0]]
                
        # Execute attacks in determined order
        for player, action in attack_actions:
            if player.active_creature.hp > 0:  # Only execute if attacker still alive
                self.execute_attack(player, action["skill"])

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

        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            choices = [SelectThing(c) for c in available_creatures]
            self._show_text(player, "Choose next creature!")
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
