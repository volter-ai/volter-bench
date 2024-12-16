from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        # Use player UIDs instead of Player objects
        self.player_queued_skill = None
        self.opponent_queued_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_choices)
            self.player_queued_skill = self.player_creature.skills[player_choices.index(player_choice)]

            # Opponent Choice Phase
            opponent_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.opponent_queued_skill = self.opponent_creature.skills[opponent_choices.index(opponent_choice)]

            # Resolution Phase
            self.resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self):
        first, second = self.determine_turn_order()
        
        # Execute first skill
        if first[0].uid == self.player.uid:
            skill = self.player_queued_skill
        else:
            skill = self.opponent_queued_skill

        damage = self.calculate_damage(
            attacker=first[1],
            defender=second[1],
            skill=skill
        )
        second[1].hp -= damage
        self._show_text(self.player, f"{first[1].display_name} used {skill.display_name} for {damage} damage!")

        # Execute second skill if creature still alive
        if second[1].hp > 0:
            if second[0].uid == self.player.uid:
                skill = self.player_queued_skill
            else:
                skill = self.opponent_queued_skill

            damage = self.calculate_damage(
                attacker=second[1],
                defender=first[1],
                skill=skill
            )
            first[1].hp -= damage
            self._show_text(self.player, f"{second[1].display_name} used {skill.display_name} for {damage} damage!")

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature), (self.opponent, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature), (self.player, self.player_creature)
        else:
            participants = [(self.player, self.player_creature), (self.opponent, self.opponent_creature)]
            random.shuffle(participants)
            return participants[0], participants[1]

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
