from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_actions = []

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player phase
            self._show_text(self.player, "Your turn!")
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent phase
            self._show_text(self.opponent, "Your turn!")
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, actor, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        return self._wait_for_choice(actor, choices).value["skill"]

    def _calculate_damage(self, attacker_skill, attacker, defender):
        # Calculate base damage
        if attacker_skill.is_physical:
            raw_damage = attacker.attack + attacker_skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * attacker_skill.base_damage
        
        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(attacker_skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, player_skill)
            second = (self.opponent, self.opponent_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first = (self.opponent, self.opponent_creature, opponent_skill)
            second = (self.player, self.player_creature, player_skill)
        else:
            options = [(self.player, self.player_creature, player_skill),
                      (self.opponent, self.opponent_creature, opponent_skill)]
            first = random.choice(options)
            second = options[1] if options[0] == first else options[0]

        # Execute moves in order
        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.opponent
                defender_creature = self.opponent_creature
            else:
                defender = self.player
                defender_creature = self.player_creature

            # Skip if attacker is fainted
            if attacker_creature.hp <= 0:
                continue

            damage = self._calculate_damage(skill, attacker_creature, defender_creature)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender_creature.display_name}!")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
