from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_turn(self.player)
            if self.check_battle_end():
                break
            self.player_turn(self.bot)
            if self.check_battle_end():
                break
            self.resolution_phase()

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill = self.choose_skill(current_player)
                if skill:
                    current_player.active_creature.chosen_skill = skill
                    return
            elif choice == swap_button:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    current_player.active_creature.chosen_skill = "swap"
                    current_player.active_creature = new_creature
                    return
            
        # Ensure a skill is chosen if the loop exits without a choice
        if not current_player.active_creature.chosen_skill:
            current_player.active_creature.chosen_skill = random.choice(current_player.active_creature.skills)

    def choose_skill(self, player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def choose_creature(self, player):
        choices = [SelectThing(creature, label=creature.display_name) 
                   for creature in player.creatures 
                   if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def resolution_phase(self):
        players = [self.player, self.bot]
        
        # Handle swaps first
        for player in players:
            if player.active_creature.chosen_skill == "swap":
                self._show_text(self.player, f"{player.display_name} swapped their active creature!")
                player.active_creature.chosen_skill = None

        # Sort players based on their active creature's speed
        players.sort(key=lambda p: (p.active_creature.speed, random.random()), reverse=True)

        for player in players:
            opponent = self.bot if player == self.player else self.player
            if player.active_creature.chosen_skill and player.active_creature.chosen_skill != "swap":
                self.execute_skill(player.active_creature, opponent.active_creature)
            
            # Check if opponent's creature fainted and force swap if necessary
            if opponent.active_creature.hp == 0:
                self.force_swap(opponent)

        self.player.active_creature.chosen_skill = None
        self.bot.active_creature.chosen_skill = None

    def execute_skill(self, attacker, defender):
        skill = attacker.chosen_skill
        if not skill or skill == "swap":
            self._show_text(self.player, f"{attacker.display_name} did nothing!")
            return

        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} and dealt {final_damage} damage to {defender.display_name}!")

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name}'s active creature fainted! They sent out {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
                creature.chosen_skill = None
