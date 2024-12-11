from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}  # Will store {player_uid: skill}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.bot.display_name}'s {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.queued_skills[self.player.uid] = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            self._show_text(self.bot, "Bot choosing skill...")
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.queued_skills[self.bot.uid] = self.bot_creature.skills[0]  # Bot always uses first skill for simplicity

            # Resolution phase
            first, second = self.determine_order()
            self.resolve_turn(first, second)

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            if attacker == self.player:
                raw_damage = self.player_creature.attack + skill.base_damage - self.bot_creature.defense
            else:
                raw_damage = self.bot_creature.attack + skill.base_damage - self.player_creature.defense
        else:
            if attacker == self.player:
                raw_damage = (self.player_creature.sp_attack / self.bot_creature.sp_defense) * skill.base_damage
            else:
                raw_damage = (self.bot_creature.sp_attack / self.player_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        if attacker == self.player:
            defender_type = self.bot_creature.creature_type
        else:
            defender_type = self.player_creature.creature_type

        effectiveness = self.get_type_effectiveness(skill.skill_type, defender_type)
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def resolve_turn(self, first, second):
        # Resolve first attacker
        if first == self.player:
            damage = self.calculate_damage(first, second, self.queued_skills[first.uid])
            self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.queued_skills[first.uid].display_name} for {damage} damage!")
        else:
            damage = self.calculate_damage(first, second, self.queued_skills[first.uid])
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.queued_skills[first.uid].display_name} for {damage} damage!")

        # Check if battle should continue
        if self.player_creature.hp > 0 and self.bot_creature.hp > 0:
            # Resolve second attacker
            if second == self.player:
                damage = self.calculate_damage(second, first, self.queued_skills[second.uid])
                self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.queued_skills[second.uid].display_name} for {damage} damage!")
            else:
                damage = self.calculate_damage(second, first, self.queued_skills[second.uid])
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.queued_skills[second.uid].display_name} for {damage} damage!")
