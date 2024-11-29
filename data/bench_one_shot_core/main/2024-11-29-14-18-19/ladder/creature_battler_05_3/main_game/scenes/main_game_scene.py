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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
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
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])
            
            if choice.display_name == "Attack":
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                if skill_choice.display_name != "Back":
                    return ("attack", next(s for s in player.active_creature.skills 
                                        if s.display_name == skill_choice.display_name))
            else:
                available = [c for c in player.creatures 
                           if c != player.active_creature and c.hp > 0]
                if not available:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                swap_choices = [Button(c.display_name) for c in available]
                swap_choices.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, swap_choices)
                if swap_choice.display_name != "Back":
                    return ("swap", next(c for c in available 
                                      if c.display_name == swap_choice.display_name))

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            first, second = self.get_action_order(
                (self.player, player_action[1]),
                (self.bot, bot_action[1])
            )
            self.execute_attack(*first)
            if self.check_battle_end():
                return
            self.execute_attack(*second)

    def execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * factor)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {target.display_name}!")
        
        if target.hp == 0:
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, target_type):
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
        
        return effectiveness.get((skill_type, target_type), 1.0)

    def get_action_order(self, action1, action2):
        p1, s1 = action1
        p2, s2 = action2
        
        speed1 = p1.active_creature.speed
        speed2 = p2.active_creature.speed
        
        if speed1 > speed2:
            return action1, action2
        elif speed2 > speed1:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def handle_knockout(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            winner = "You" if player == self.bot else "The foe"
            self._show_text(self.player, f"{winner} won the battle!")
            return
            
        self._show_text(self.player, 
            f"{player.active_creature.display_name} was knocked out!")
        
        swap_choices = [Button(c.display_name) for c in available]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = next(c for c in available 
                                    if c.display_name == choice.display_name)

    def check_battle_end(self):
        for p in [self.player, self.bot]:
            if not any(c.hp > 0 for c in p.creatures):
                return True
        return False
