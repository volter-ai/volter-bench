from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}  # Will store prototype_ids instead of Thing objects

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature)}
"""

    def _format_skills(self, creature):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {'physical' if skill.is_physical else 'special'})" 
                         for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player phase
            self._show_text(self.player, "Your turn! Choose a skill:")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            self.queued_skills[self.player.prototype_id] = player_skill

            # Bot phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing
            self.queued_skills[self.bot.prototype_id] = bot_skill

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        for attacker in [first, second]:
            if attacker == self.player:
                defender_creature = self.bot_creature
            else:
                defender_creature = self.player_creature

            skill = self.queued_skills[attacker.prototype_id]
            damage = self._calculate_damage(
                attacker.creatures[0], 
                defender_creature,
                skill
            )
            
            defender_creature.hp = max(0, defender_creature.hp - damage)
            self._show_text(self.player, 
                f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name} for {damage} damage!")

    def _determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
