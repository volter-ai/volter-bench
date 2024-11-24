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

Your other creatures: {', '.join(c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0)}
Foe's other creatures: {', '.join(c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0)}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_turn_action(self.player)
            bot_action = self.get_turn_action(self.bot)
            
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

    def get_turn_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choices = [attack, swap]
            
            choice = self._wait_for_choice(player, choices)
            
            if choice == attack:
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                if skill_choice.display_name != "Back":
                    return ("attack", skill_choice.display_name)
            
            elif choice == swap:
                available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if available:
                    swap_choices = [SelectThing(c) for c in available]
                    swap_choices.append(Button("Back"))
                    swap_choice = self._wait_for_choice(player, swap_choices)
                    if not isinstance(swap_choice, Button):
                        return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, action[1])
                
                # Force swap if creature fainted
                if defender.active_creature.hp <= 0:
                    available = [c for c in defender.creatures if c.hp > 0]
                    if available:
                        swap_choices = [SelectThing(c) for c in available]
                        swap_choice = self._wait_for_choice(defender, swap_choices)
                        defender.active_creature = swap_choice.thing
                        self._show_text(defender, f"{defender.display_name} sent out {swap_choice.thing.display_name}!")

    def execute_attack(self, attacker, defender, skill_name):
        skill = next(s for s in attacker.active_creature.skills if s.display_name == skill_name)
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if effectiveness > 1:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness < 1:
            self._show_text(attacker, "It's not very effective...")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness.get((skill_type, creature_type), 1.0)

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
        return False
