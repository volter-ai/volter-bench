from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Action, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Keep asking for choice until a valid action is selected (not Back)
            while True:
                player_choice = self.get_player_choice(self.player)
                if player_choice is not None:
                    player_action = self.create_action(player_choice, self.player)
                    break
            
            bot_action = self.create_action(self.get_player_choice(self.bot), self.bot)
            
            self.resolve_turn(player_action, bot_action)
            
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_choice(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Add Back button to skills menu
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            choice = self._wait_for_choice(player, skill_choices + [back_button])
            if choice == back_button:
                return None
            return choice
        else:
            # Add Back button to creature menu
            available_creatures = [c for c in player.creatures if c.hp > 0]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            choice = self._wait_for_choice(player, creature_choices + [back_button])
            if choice == back_button:
                return None
            return choice

    def create_action(self, choice: SelectThing, player: Player) -> Action:
        return Action(
            display_name=f"{player.display_name}'s action",
            description="A battle action",
            prototype_id=f"action_{player.uid}",
            acting_player=player,
            target_thing=choice.thing
        )

    def resolve_turn(self, player_action: Action, bot_action: Action):
        first_action, second_action = self.determine_action_order(player_action, bot_action)
        self.execute_action(first_action)
        self.execute_action(second_action)

    def determine_action_order(self, player_action: Action, bot_action: Action):
        if isinstance(player_action.target_thing, Creature) and not isinstance(bot_action.target_thing, Creature):
            return player_action, bot_action
        elif isinstance(bot_action.target_thing, Creature) and not isinstance(player_action.target_thing, Creature):
            return bot_action, player_action
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action: Action):
        if isinstance(action.target_thing, Creature):
            if action.target_thing != action.acting_player.active_creature:
                if action.acting_player == self.player:
                    self.player.active_creature = action.target_thing
                else:
                    self.bot.active_creature = action.target_thing
        else:
            skill = action.target_thing
            attacker = self.player.active_creature if action.acting_player == self.player else self.bot.active_creature
            defender = self.bot.active_creature if action.acting_player == self.player else self.player.active_creature
            
            damage = self.calculate_damage(skill, attacker, defender)
            defender.hp = max(0, defender.hp - damage)
            
            if defender.hp == 0:
                self.handle_fainted_creature(defender)

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type: str, defend_type: str):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_fainted_creature(self, fainted_creature: Creature):
        player = self.player if fainted_creature in self.player.creatures else self.bot
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
