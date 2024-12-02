from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase  
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Resolution Phase
            self._resolve_turn(player_skill, bot_skill)
            
            if self._check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _resolve_turn(self, player_skill, bot_skill):
        # Determine order
        first, second = self._determine_order(
            (self.player, self.player_creature, player_skill),
            (self.bot, self.bot_creature, bot_skill)
        )

        # Execute skills in order
        self._execute_skill(*first)
        if self._check_battle_end():
            return
        self._execute_skill(*second)

    def _determine_order(self, action1, action2):
        player1, creature1, _ = action1
        player2, creature2, _ = action2
        
        if creature1.speed > creature2.speed:
            return action1, action2
        elif creature2.speed > creature1.speed:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.bot
            defender_creature = self.bot_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self._get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)

        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False
