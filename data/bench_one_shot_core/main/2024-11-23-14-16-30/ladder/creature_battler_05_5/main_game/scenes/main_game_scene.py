from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return self.get_player_action(player)
            
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]

        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first[0], first[1])
        if second[0].active_creature.hp > 0:
            self.execute_action(second[0], second[1])

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (self.player, player_action), (self.bot, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return (self.bot, bot_action), (self.player, player_action)
        else:
            if random.random() < 0.5:
                return (self.player, player_action), (self.bot, bot_action)
            return (self.bot, bot_action), (self.player, player_action)

    def execute_action(self, attacker, action):
        if action["type"] != "attack":
            return
            
        skill = action["skill"]
        defender = self.bot if attacker == self.player else self.player
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {target.display_name}!")

        if target.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if player_alive else "Bot"
            self._show_text(self.player, f"{winner} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
