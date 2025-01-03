import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_battle()

    def _initialize_battle(self):
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
> Swap"""

    def _get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn_choice(self, player: Player) -> tuple[str, Creature | None, str | None]:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])

        if choice == attack_button:
            skill_choices = [Button(skill.display_name) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self._handle_turn_choice(player)
            return "attack", None, skill_choice.display_name.lower()
        else:
            available = self._get_available_creatures(player)
            if not available:
                return "none", None, None
                
            creature_choices = [SelectThing(c) for c in available]
            back_button = Button("Back")
            swap_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if swap_choice == back_button:
                return self._handle_turn_choice(player)
            return "swap", swap_choice.thing, None

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill_name: str) -> int:
        skill = next(s for s in attacker.skills if s.display_name.lower() == skill_name)
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                effectiveness = 2.0
            elif defender.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                effectiveness = 2.0
            elif defender.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                effectiveness = 2.0
            elif defender.creature_type == "fire":
                effectiveness = 0.5
                
        return int(raw_damage * effectiveness)

    def _handle_forced_swap(self, player: Player):
        available = self._get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        swap_choice = self._wait_for_choice(player, [SelectThing(c) for c in available])
        player.active_creature = swap_choice.thing
        return True

    def run(self):
        while True:
            # Player turn choice
            player_action, player_swap, player_skill = self._handle_turn_choice(self.player)
            
            # Bot turn choice 
            bot_action, bot_swap, bot_skill = self._handle_turn_choice(self.bot)
            
            # Resolution phase
            if player_action == "swap":
                self.player.active_creature = player_swap
                
            if bot_action == "swap":
                self.bot.active_creature = bot_swap
                
            # Determine attack order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = self.player, self.bot
                first_skill, second_skill = player_skill, bot_skill
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = self.bot, self.player
                first_skill, second_skill = bot_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player, self.bot
                    first_skill, second_skill = player_skill, bot_skill
                else:
                    first, second = self.bot, self.player
                    first_skill, second_skill = bot_skill, player_skill
                    
            # Execute attacks
            if first_skill:
                damage = self._calculate_damage(first.active_creature, second.active_creature, first_skill)
                second.active_creature.hp = max(0, second.active_creature.hp - damage)
                self._show_text(first, f"{first.active_creature.display_name} used {first_skill}!")
                self._show_text(second, f"{second.active_creature.display_name} took {damage} damage!")
                
                if second.active_creature.hp == 0:
                    if not self._handle_forced_swap(second):
                        self._show_text(self.player, "You win!" if second == self.bot else "You lose!")
                        self._quit_whole_game()
                        
            if second_skill:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_skill)
                first.active_creature.hp = max(0, first.active_creature.hp - damage)
                self._show_text(second, f"{second.active_creature.display_name} used {second_skill}!")
                self._show_text(first, f"{first.active_creature.display_name} took {damage} damage!")
                
                if first.active_creature.hp == 0:
                    if not self._handle_forced_swap(first):
                        self._show_text(self.player, "You win!" if first == self.bot else "You lose!")
                        self._quit_whole_game()
