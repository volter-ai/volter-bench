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
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game when battle is over

    def get_player_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])
            
            if choice == attack:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice != back:
                    return ("attack", skill_choice.thing)
            else:
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if available:
                    creatures = [SelectThing(c) for c in available]
                    back = Button("Back")
                    creature_choice = self._wait_for_choice(player, creatures + [back])
                    if creature_choice != back:
                        return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        if self.player.active_creature.speed < self.bot.active_creature.speed:
            actions.reverse()
        elif self.player.active_creature.speed == self.bot.active_creature.speed:
            if random.random() < 0.5:
                actions.reverse()

        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker.active_creature, defender.active_creature, action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * factor)
        defender.hp = max(0, defender.hp - final_damage)

        # Show damage text
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

        if defender.hp == 0:
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, knocked_out_creature):
        owner = self.player if knocked_out_creature in self.player.creatures else self.bot
        self._show_text(self.player, f"{knocked_out_creature.display_name} was knocked out!")
        
        available = [c for c in owner.creatures if c.hp > 0]
        if available:
            if owner == self.player:
                choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(owner, choices)
                owner.active_creature = choice.thing
            else:
                owner.active_creature = available[0]
        
    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = "You win!" if p_alive else "You lose!"
            self._show_text(self.player, winner)
            return True
        return False
