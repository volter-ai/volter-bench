from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

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
{"> Swap" if self.has_available_swaps(self.player) else ""}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After battle ends, ask player if they want to play again
                play_again = Button("Play Again")
                quit_game = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again, quit_game])
                
                if choice == play_again:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def has_available_swaps(self, player):
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def force_creature_swap(self, player):
        """Forces player to swap their active creature if it's knocked out"""
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                choice = self._wait_for_choice(player, creature_choices)
                player.active_creature = choice.thing

    def get_player_action(self, player):
        # First check if we need to force a swap
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                return self._wait_for_choice(player, creature_choices)
            return None  # No available creatures means battle will end

        # Normal turn choices
        choices = [Button("Attack")]
        if self.has_available_swaps(player):
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills with back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choices.append(back_button)
            
            while True:
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    return self.get_player_action(player)
                return skill_choice
        else:
            # Show available creatures with back option
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choices.append(back_button)
            
            while True:
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    return self.get_player_action(player)
                return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing

        # Determine order for attacks
        first = self.player if self.player.active_creature.speed >= self.bot.active_creature.speed else self.bot
        second = self.bot if first == self.player else self.player
        first_action = player_action if first == self.player else bot_action
        second_action = bot_action if first == self.player else player_action

        # Execute first attack and check for knockouts
        if isinstance(first_action.thing, Skill):
            self.execute_attack(first, second, first_action.thing)
            self.force_creature_swap(second)  # Check if defender needs to swap

        # Execute second attack only if the creature is still alive
        if isinstance(second_action.thing, Skill) and second.active_creature.hp > 0:
            self.execute_attack(second, first, second_action.thing)
            self.force_creature_swap(first)  # Check if defender needs to swap

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

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
