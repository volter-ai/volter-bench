from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
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
        while True:
            # Check if either player has no valid moves before continuing
            if not self.has_valid_moves(self.player):
                self._show_text(self.player, f"{self.bot.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return
            if not self.has_valid_moves(self.bot):
                self._show_text(self.player, f"{self.player.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return

            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def has_valid_moves(self, player):
        return (player.active_creature and player.active_creature.hp > 0) or any(c.hp > 0 for c in player.creatures if c != player.active_creature)

    def get_player_action(self, player):
        if not player.active_creature or player.active_creature.hp <= 0:
            # Must swap if active creature is fainted
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if not valid_creatures:
                return None
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
            return SelectThing(new_creature)

        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            main_choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if main_choice == attack_button:
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                choices.append(back_button)
                
                choice = self._wait_for_choice(player, choices)
                if choice == back_button:
                    continue
                return choice
            else:
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not valid_creatures:
                    # If no valid creatures to swap to, force attack
                    choices = [SelectThing(skill) for skill in player.active_creature.skills]
                    back_button = Button("Back")
                    choices.append(back_button)
                    
                    choice = self._wait_for_choice(player, choices)
                    if choice == back_button:
                        continue
                    return choice
                    
                choices = [SelectThing(creature) for creature in valid_creatures]
                back_button = Button("Back")
                choices.append(back_button)
                
                choice = self._wait_for_choice(player, choices)
                if choice == back_button:
                    continue
                return choice

    def resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return

        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed, with random tiebreaker
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        for actor, action in actions:
            if isinstance(action.thing, type(self.player.creatures[0].skills[0])):
                skill = action.thing
                target = self.bot if actor == self.player else self.player
                damage = self.calculate_damage(actor.active_creature, target.active_creature, skill)
                target.active_creature.hp = max(0, target.active_creature.hp - damage)
                
                self._show_text(self.player, f"{actor.active_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")

                if target.active_creature.hp == 0:
                    self.handle_fainted_creature(target)

    def calculate_damage(self, attacker, defender, skill):
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

    def handle_fainted_creature(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
