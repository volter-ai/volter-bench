from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.player_action = ""
        self.bot_action = ""

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        player_hp = f"(HP: {player_creature.hp}/{player_creature.max_hp})" if player_creature else "(Defeated)"
        bot_hp = f"(HP: {bot_creature.hp}/{bot_creature.max_hp})" if bot_creature else "(Defeated)"
        
        return f"""===Battle===
{self.player.display_name}: {player_creature.display_name if player_creature else 'No active creature'} {player_hp}
{self.bot.display_name}: {bot_creature.display_name if bot_creature else 'No active creature'} {bot_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return
            self.player_turn()
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return
            self.bot_turn()
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return
            self.resolution_phase()

    def player_turn(self):
        self.player_action = self.get_player_action(self.player)

    def bot_turn(self):
        self.bot_action = self.get_player_action(self.bot)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self.choose_skill(player)
                if skill:
                    return f"attack:{skill.prototype_id}"
                else:
                    return "attack:struggle"  # Default to struggle if no skill is chosen
            elif choice == swap_button:
                creature = self.choose_creature(player)
                if creature:
                    return f"swap:{creature.prototype_id}"
                else:
                    return "attack:struggle"  # Default to struggle if no creature is chosen for swap

    def choose_skill(self, player):
        if not player.active_creature:
            return None
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        if not skills:
            return None  # No skills available
        back_button = Button("Back")
        choices = skills + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def choose_creature(self, player):
        creatures = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        if not creatures:
            return None  # No creatures available to swap
        back_button = Button("Back")
        choices = creatures + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def resolution_phase(self):
        actions = [
            (self.player, self.player_action),
            (self.bot, self.bot_action)
        ]

        # Sort actions based on speed or swap priority
        actions.sort(key=lambda x: (
            0 if x[1].startswith("swap") else 1,
            -x[0].active_creature.speed if x[0].active_creature else 0
        ))

        for player, action in actions:
            if action.startswith("swap"):
                _, creature_id = action.split(":")
                new_creature = next((c for c in player.creatures if c.prototype_id == creature_id), None)
                self.perform_swap(player, new_creature)
            elif action.startswith("attack"):
                _, skill_id = action.split(":")
                if skill_id == "struggle":
                    self.perform_struggle(player)
                else:
                    skill = next((s for s in player.active_creature.skills if s.prototype_id == skill_id), None)
                    self.perform_attack(player, skill)

    def perform_swap(self, player, new_creature):
        if new_creature:
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures to swap!")

    def perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        if not attacker.active_creature or not defender.active_creature:
            return
        if skill is None:
            self.perform_struggle(attacker)
            return
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def perform_struggle(self, attacker):
        defender = self.bot if attacker == self.player else self.player
        if not attacker.active_creature or not defender.active_creature:
            return
        damage = max(1, attacker.active_creature.attack // 2)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        attacker.active_creature.hp = max(0, attacker.active_creature.hp - damage // 2)
        self._show_text(self.player, f"{attacker.active_creature.display_name} struggled and dealt {damage} damage to {defender.active_creature.display_name}!")
        self._show_text(self.player, f"{attacker.active_creature.display_name} took {damage // 2} recoil damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)
        if attacker.active_creature.hp == 0:
            self._show_text(self.player, f"{attacker.active_creature.display_name} fainted!")
            self.force_swap(attacker)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = self.choose_creature(player)
            self.perform_swap(player, new_creature)
        else:
            player.active_creature = None
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        if not self.player.active_creature or all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if not self.bot.active_creature or all(creature.hp <= 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
