from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.game_over = False
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while not self.game_over:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self.game_over = True
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self.game_over = True
                continue

            # Resolve actions
            self.resolve_turn(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                self.game_over = True
                continue

        # When game is over, transition back to menu
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button, back_button])
            
            if choice == back_button:
                if player == self.bot:  # Bot shouldn't go back
                    continue
                return None
            
            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if isinstance(skill_choice, Button):  # Back was chosen
                    continue
                    
                return ("attack", skill_choice.thing)
            else:  # Swap chosen
                valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not valid_creatures:
                    return None
                    
                creature_choices = [SelectThing(creature) for creature in valid_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, creature_choices)
                
                if isinstance(creature_choice, Button):  # Back was chosen
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Resolve swaps first
        for player, (action_type, target) in actions:
            if action_type == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")

        # Then resolve attacks
        # Sort by speed, with random resolution for ties
        def get_speed_key(player_action_tuple):
            player, _ = player_action_tuple
            return (player.active_creature.speed, random.random())
            
        actions.sort(key=get_speed_key, reverse=True)
        
        for player, (action_type, target) in actions:
            if action_type == "attack":
                defender = self.bot if player == self.player else self.player
                damage = self.calculate_damage(target, player.active_creature, defender.active_creature)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, f"{player.active_creature.display_name} used {target.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")

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
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        def has_conscious_creatures(player):
            return any(c.hp > 0 for c in player.creatures)

        player_can_continue = has_conscious_creatures(self.player)
        bot_can_continue = has_conscious_creatures(self.bot)

        if not player_can_continue or not bot_can_continue:
            winner = self.player if player_can_continue else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True

        # Force swap if active creature is fainted
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                valid_creatures = [c for c in player.creatures if c.hp > 0]
                if valid_creatures:
                    choices = [SelectThing(c) for c in valid_creatures]
                    new_creature = self._wait_for_choice(player, choices).thing
                    player.active_creature = new_creature
                    self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")

        return False
