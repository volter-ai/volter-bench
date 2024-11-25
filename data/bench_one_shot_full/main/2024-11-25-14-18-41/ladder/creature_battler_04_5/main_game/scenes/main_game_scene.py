from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Phase: {self.phase}

Available Skills:
{self._format_skills()}
"""

    def _format_skills(self):
        if self.phase == "player_choice":
            return "\n".join(f"> {skill.display_name}" for skill in self.player_creature.skills)
        return ""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player choice phase
            self.phase = "player_choice"
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            self.queued_skills[self.player.prototype_id] = player_skill

            # Bot choice phase
            self.phase = "bot_choice"
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing
            self.queued_skills[self.bot.prototype_id] = bot_skill

            # Resolution phase
            self.phase = "resolution"
            self._resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        first, second = self._determine_order()
        
        self._execute_skill(first, self.queued_skills[first.prototype_id])
        if self.player_creature.hp > 0 and self.bot_creature.hp > 0:
            self._execute_skill(second, self.queued_skills[second.prototype_id])

    def _determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def _execute_skill(self, attacker, skill):
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.bot_creature
        else:
            attacker_creature = self.bot_creature
            defender_creature = self.player_creature

        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)

        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
