import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures = "\n".join(
            f"{'[ACTIVE] ' if c == self.player.active_creature else ''}{c.display_name} - HP: {c.hp}/{c.max_hp}"
            for c in self.player.creatures
        )
        bot_creatures = "\n".join(
            f"{'[ACTIVE] ' if c == self.bot.active_creature else ''}{c.display_name} - HP: {c.hp}/{c.max_hp}"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle Scene ===
Your Creatures:
{player_creatures}

Opponent's Creatures:
{bot_creatures}

Options:
> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Check battle end before each turn
            if self.check_battle_end():
                return
                
            # Player turn
            player_action = self.get_player_action(self.player, "player")
            if not player_action:
                if self.check_battle_end():
                    return
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot, "bot")
            if not bot_action:
                if self.check_battle_end():
                    return
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def check_battle_end(self):
        """Returns True if battle ended, False otherwise"""
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if bot_alive else "The opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False

    def get_player_action(self, player, player_id):
        # First check if current creature is knocked out and needs replacing
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            return None  # Return None to skip turn after swapping

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.get_player_action(player, player_id)
                
            return ("attack", skill_choice.thing, player_id)
            
        else:
            # Show available creatures
            available_creatures = [
                c for c in player.creatures 
                if c != player.active_creature and c.hp > 0
            ]
            if not available_creatures:
                self._show_text(player, "No other creatures available to swap to!")
                return self.get_player_action(player, player_id)
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self.get_player_action(player, player_id)
                
            return ("swap", creature_choice.thing, player_id)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        self.execute_action(first_action)
        
        # Check battle end between actions
        if self.check_battle_end():
            return
            
        self.execute_action(second_action)
        
        # Check battle end after actions
        self.check_battle_end()

    def execute_action(self, action):
        if not action or action[0] != "attack":
            return
            
        skill = action[1]
        attacker = self.player if action[2] == "player" else self.bot
        defender = self.bot if action[2] == "player" else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def get_action_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return (player_action, bot_action)
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (player_action, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return (bot_action, player_action)
        else:
            if random.random() < 0.5:
                return (player_action, bot_action)
            else:
                return (bot_action, player_action)
