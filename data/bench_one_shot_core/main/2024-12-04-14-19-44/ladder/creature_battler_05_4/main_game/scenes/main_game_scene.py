from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break
                
        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None
            
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            skills = [SelectThing(s) for s in player.active_creature.skills]
            back = Button("Back")
            skill_choice = self._wait_for_choice(player, skills + [back])
            if skill_choice == back:
                return self.get_player_action(player)
            return ("attack", skill_choice.thing)
            
        else:
            available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            creatures = [SelectThing(c) for c in available]
            back = Button("Back")
            creature_choice = self._wait_for_choice(player, creatures + [back])
            if creature_choice == back:
                return self.get_player_action(player)
            return ("swap", creature_choice.thing)

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        actions = [(p1_action, self.player, self.bot), (p2_action, self.bot, self.player)]
        
        # Sort by speed
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if action[0] == "attack":
                skill = action[1]
                damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")

                if defender.active_creature.hp == 0:
                    self._show_text(self.player, 
                        f"{defender.display_name}'s {defender.active_creature.display_name} was knocked out!")
                    
                    available = [c for c in defender.creatures if c.hp > 0]
                    if available:
                        if defender == self.player:
                            swap_choice = self._wait_for_choice(defender, 
                                [SelectThing(c) for c in available])
                            defender.active_creature = swap_choice.thing
                        else:
                            defender.active_creature = random.choice(available)
                        
                        self._show_text(self.player,
                            f"{defender.display_name} sent out {defender.active_creature.display_name}!")

    def calculate_damage(self, skill, attacker, defender):
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
            
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness.get((attack_type, defend_type), 1.0)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(c.hp > 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
