from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Choose your skill!")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            self.queued_skills[self.player.uid] = player_skill

            # Bot Choice Phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing
            self.queued_skills[self.bot.uid] = bot_skill

            # Resolution Phase
            self.resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def resolve_turn(self):
        first, second = self.get_turn_order()
        
        # Execute first skill
        damage = self.calculate_damage(
            attacker=first[0].creatures[0],
            defender=second[0].creatures[0],
            skill=first[1]
        )
        second[0].creatures[0].hp -= damage
        self._show_text(self.player, 
            f"{first[0].display_name}'s {first[0].creatures[0].display_name} used {first[1].display_name} for {damage} damage!")

        # Execute second skill if creature still alive
        if second[0].creatures[0].hp > 0:
            damage = self.calculate_damage(
                attacker=second[0].creatures[0],
                defender=first[0].creatures[0],
                skill=second[1]
            )
            first[0].creatures[0].hp -= damage
            self._show_text(self.player,
                f"{second[0].display_name}'s {second[0].creatures[0].display_name} used {second[1].display_name} for {damage} damage!")

    def get_turn_order(self):
        player_speed = self.player_creature.speed
        bot_speed = self.bot_creature.speed
        
        if player_speed > bot_speed:
            return (self.player, self.queued_skills[self.player.uid]), (self.bot, self.queued_skills[self.bot.uid])
        elif bot_speed > player_speed:
            return (self.bot, self.queued_skills[self.bot.uid]), (self.player, self.queued_skills[self.player.uid])
        else:
            actors = [(self.player, self.queued_skills[self.player.uid]), (self.bot, self.queued_skills[self.bot.uid])]
            random.shuffle(actors)
            return actors[0], actors[1]

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * type_factor)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
