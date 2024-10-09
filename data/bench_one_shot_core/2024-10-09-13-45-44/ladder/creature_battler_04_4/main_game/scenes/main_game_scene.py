from mini_game_engine.engine.lib import AbstractGameScene, Button, create_from_game_database
from main_game.models import Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_player("opponent")
        self.player_creature = None
        self.opponent_creature = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{self._get_skill_choices_str()}
"""

    def _get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._initialize_battle()
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player_creature = create_from_game_database(self.player.creatures[0].prototype_id, Creature)
        self.opponent_creature = create_from_game_database(self.opponent.creatures[0].prototype_id, Creature)

    def game_loop(self):
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()

            first, second = self._determine_turn_order(player_skill, opponent_skill)
            self._resolve_turn(first)
            if self._check_battle_end():
                break
            self._resolve_turn(second)
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, choices)

    def _determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill), (self.opponent, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill), (self.player, player_skill)
        else:
            coin_flip = self._app.random.randint(0, 1)
            if coin_flip == 0:
                return (self.player, player_skill), (self.opponent, opponent_skill)
            else:
                return (self.opponent, opponent_skill), (self.player, player_skill)

    def _resolve_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack * skill.base_damage) // defender.sp_defense

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type: str, defender_type: str) -> int:
        if skill_type == defender_type:
            return 1
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0
        else:
            return 1

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False
