from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}

> Attack
> Swap"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._get_player_action(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _get_player_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])

            if choice == attack:
                # Create parallel lists of buttons and skills
                skill_buttons = []
                skills = []
                for skill in player.active_creature.skills:
                    skill_buttons.append(Button(skill.display_name))
                    skills.append(skill)
                
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_buttons + [back])
                if skill_choice == back:
                    continue
                    
                # Find the index of the chosen button and use it to get the skill
                skill_index = skill_buttons.index(skill_choice)
                chosen_skill = skills[skill_index]
                return ("attack", chosen_skill, player)
                
            elif choice == swap:
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                swap_choices = [SelectThing(c) for c in available_creatures]
                back = Button("Back")
                swap_choice = self._wait_for_choice(player, swap_choices + [back])
                if swap_choice == back:
                    continue
                return ("swap", swap_choice.thing, player)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        first, second = self._determine_order(player_action, bot_action)
        self._execute_action(first)
        if self._check_battle_end():
            return
        self._execute_action(second)

    def _determine_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return (player_action, bot_action)
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (player_action, bot_action)
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            return (bot_action, player_action)
        else:
            import random
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def _execute_action(self, action):
        if action[0] == "attack":
            action_type, skill, attacker = action
            defender = self.bot if attacker == self.player else self.player
            
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                swap_choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(self.player, swap_choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp <= 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                import random
                self.bot.active_creature = random.choice(available)
                
        return False
