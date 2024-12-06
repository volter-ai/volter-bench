from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.opponent)
            if not bot_action:
                continue

            # Resolve actions
            self.resolve_turn(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        choice = self._wait_for_choice(player, [attack_button, swap_button])

        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)

        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
            
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.opponent, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks based on speed
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            first, second = actions
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            second, first = actions
        else:
            if random.random() < 0.5:
                first, second = actions
            else:
                second, first = actions

        for attacker, action in [first, second]:
            if action[0] == "attack":
                self.execute_attack(attacker, action[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.opponent
        else:
            defender = self.player

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)

        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if effectiveness == 2:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness == 0.5:
            self._show_text(attacker, "It's not very effective...")

        # Handle KO
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature:")
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)

        if not player_alive or not opponent_alive:
            winner = self.player if player_alive else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            
            # Reset creatures
            for creature in self.player.creatures + self.opponent.creatures:
                creature.hp = creature.max_hp
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
