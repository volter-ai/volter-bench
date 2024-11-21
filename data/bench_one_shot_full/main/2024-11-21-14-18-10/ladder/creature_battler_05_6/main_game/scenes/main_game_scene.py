from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._initialize_creatures()

    def _initialize_creatures(self):
        # Reset creatures to starting state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def _get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _execute_turn(self, first_player, first_action, second_player, second_action):
        # Handle swaps first
        if isinstance(first_action, Creature):
            first_player.active_creature = first_action
        if isinstance(second_action, Creature):
            second_player.active_creature = second_action

        # Then handle attacks
        if not isinstance(first_action, Creature):
            damage = self._calculate_damage(first_player.active_creature, second_player.active_creature, first_action)
            second_player.active_creature.hp -= damage
            self._show_text(first_player, f"{first_player.active_creature.display_name} used {first_action.display_name}!")
            self._show_text(second_player, f"{first_player.active_creature.display_name} used {first_action.display_name}!")

        if second_player.active_creature.hp > 0 and not isinstance(second_action, Creature):
            damage = self._calculate_damage(second_player.active_creature, first_player.active_creature, second_action)
            first_player.active_creature.hp -= damage
            self._show_text(first_player, f"{second_player.active_creature.display_name} used {second_action.display_name}!")
            self._show_text(second_player, f"{second_player.active_creature.display_name} used {second_action.display_name}!")

    def _handle_player_turn(self, player: Player) -> any:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                if skill_choice != back_button:
                    return skill_choice.thing
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c.hp > 0 and c != player.active_creature
                ]
                back_button = Button("Back")
                swap_choice = self._wait_for_choice(player, available_creatures + [back_button])
                if swap_choice != back_button:
                    return swap_choice.thing

    def _force_swap(self, player: Player):
        available_creatures = [
            SelectThing(c) for c in player.creatures 
            if c.hp > 0
        ]
        if not available_creatures:
            return False
            
        swap_choice = self._wait_for_choice(player, available_creatures)
        player.active_creature = swap_choice.thing
        return True

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_turn(self.player)
            bot_action = self._handle_player_turn(self.bot)

            # Determine turn order
            if (isinstance(player_action, Creature) and isinstance(bot_action, Creature)) or \
               (not isinstance(player_action, Creature) and not isinstance(bot_action, Creature)):
                if self.player.active_creature.speed >= self.bot.active_creature.speed:
                    first_player, first_action = self.player, player_action
                    second_player, second_action = self.bot, bot_action
                else:
                    first_player, first_action = self.bot, bot_action
                    second_player, second_action = self.player, player_action
            elif isinstance(player_action, Creature):
                first_player, first_action = self.player, player_action
                second_player, second_action = self.bot, bot_action
            else:
                first_player, first_action = self.bot, bot_action
                second_player, second_action = self.player, player_action

            self._execute_turn(first_player, first_action, second_player, second_action)

            # Handle knockouts
            if self.player.active_creature.hp <= 0:
                if not self._force_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    self._show_text(self.bot, "You won!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self._force_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    self._show_text(self.bot, "You lost!")
                    break

        self._transition_to_scene("MainMenuScene")
