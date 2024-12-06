from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal" or defender_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_turn(self, player: Player, opponent: Player):
        # Get player action
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])

        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill = self._wait_for_choice(player, skill_choices).thing
            return ("attack", skill)
        else:
            # Show available creatures
            available = self.get_available_creatures(player)
            if not available:
                return None
            creature_choices = [SelectThing(creature) for creature in available]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            return ("swap", new_creature)

    def run(self):
        while True:
            # Player turn
            player_action = self.handle_turn(self.player, self.bot)
            if not player_action:
                self._show_text(self.player, "You have no more creatures!")
                self._show_text(self.player, "You lose!")
                self._transition_to_scene("MainMenuScene")
                return

            # Bot turn
            bot_action = self.handle_turn(self.bot, self.player)
            if not bot_action:
                self._show_text(self.player, "Opponent has no more creatures!")
                self._show_text(self.player, "You win!")
                self._transition_to_scene("MainMenuScene")
                return

            # Resolve actions
            actions = [(self.player, player_action), (self.bot, bot_action)]
            
            # Handle swaps first
            for player, action in actions:
                if action[0] == "swap":
                    player.active_creature = action[1]
                    self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")

            # Then handle attacks
            random.shuffle(actions)  # Randomize order for same speed
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

            for player, action in actions:
                if action[0] == "attack":
                    opponent = self.bot if player == self.player else self.player
                    damage = self.calculate_damage(player.active_creature, opponent.active_creature, action[1])
                    opponent.active_creature.hp -= damage
                    self._show_text(self.player, 
                        f"{player.display_name}'s {player.active_creature.display_name} used {action[1].display_name}! "
                        f"Dealt {damage} damage!")

                    if opponent.active_creature.hp <= 0:
                        opponent.active_creature.hp = 0
                        self._show_text(self.player, 
                            f"{opponent.display_name}'s {opponent.active_creature.display_name} was knocked out!")
                        
                        available = self.get_available_creatures(opponent)
                        if not available:
                            self._show_text(self.player, 
                                "You win!" if opponent == self.bot else "You lose!")
                            self._transition_to_scene("MainMenuScene")
                            return
                        
                        if opponent == self.player:
                            creature_choices = [SelectThing(creature) for creature in available]
                            new_creature = self._wait_for_choice(self.player, creature_choices).thing
                        else:
                            new_creature = random.choice(available)
                        
                        opponent.active_creature = new_creature
                        self._show_text(self.player, 
                            f"{opponent.display_name} sent out {new_creature.display_name}!")
