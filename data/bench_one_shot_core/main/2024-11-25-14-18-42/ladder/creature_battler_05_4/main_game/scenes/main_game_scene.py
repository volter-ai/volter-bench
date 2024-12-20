from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_creatures()

    def _initialize_creatures(self):
        # Reset creatures and set initial active creatures
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
{"> Swap" if self._get_available_creatures(self.player) else ""}
"""

    def _get_damage_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type or skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_damage_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _execute_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action, Creature):
            self.player.active_creature = player_action
        if isinstance(bot_action, Creature):
            self.bot.active_creature = bot_action

        # Then handle attacks based on speed
        if isinstance(player_action, Creature) and isinstance(bot_action, Creature):
            return
            
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = second, first
            first_action, second_action = second_action, first_action
            
        if isinstance(first_action, Creature):
            damage = self._calculate_damage(second.active_creature, first.active_creature, second_action)
            first.active_creature.hp -= damage
        else:
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp -= damage
            
        if isinstance(second_action, Creature):
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp -= damage
        else:
            damage = self._calculate_damage(second.active_creature, first.active_creature, second_action)
            first.active_creature.hp -= damage

    def _get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def _handle_fainted(self, player: Player) -> bool:
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
                
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def run(self):
        while True:
            # Build choice list based on available options
            choices = [Button("Attack")]
            available_creatures = self._get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            # Player turn
            player_choice = self._wait_for_choice(self.player, choices)
            
            if player_choice.display_name == "Attack":
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                player_action = self._wait_for_choice(self.player, skill_choices).thing
            else:
                creature_choices = [SelectThing(c) for c in available_creatures]
                player_action = self._wait_for_choice(self.player, creature_choices).thing

            # Bot turn
            bot_action = self.bot.active_creature.skills[0]  # Simple AI just uses first skill
            
            # Execute turn
            self._execute_turn(player_action, bot_action)
            
            # Check for fainted creatures
            if not self._handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self._handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break
                
        self._transition_to_scene("MainMenuScene")
