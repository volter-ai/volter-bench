from main_game.models import Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("bot_player")
        self.player_score = 0
        self.bot_score = 0
        self.rounds = 0

    def run(self):
        self._show_text(self.player, "Welcome to the Rock Paper Scissors game!")
        
        while self.player_score < 2 and self.bot_score < 2 and self.rounds < 3:
            self._play_round()

        self._show_results()

        choice = self._wait_for_choice(self.player, [
            Button("Play Again"),
            Button("Quit")
        ])

        if choice.display_name == "Play Again":
            self._transition_to_scene("MainGameScene")
        else:
            self._transition_to_scene("MainMenuScene")

    def _play_round(self):
        self.rounds += 1
        self._show_text(self.player, f"Round {self.rounds}")

        human_player_skill = self._get_player_skill(self.player)
        bot_skill = self._get_player_skill(self.bot)

        self._show_text(self.player, f"You chose {human_player_skill.display_name}")
        self._show_text(self.player, f"Bot chose {bot_skill.display_name}")

        result = self._determine_winner(human_player_skill, bot_skill)
        self._show_text(self.player, result)

    def _get_player_skill(self, player: Player):
        choices = [SelectThing(thing=skill) for skill in player.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _determine_winner(self, player_skill, bot_skill):
        if player_skill.display_name == bot_skill.display_name:
            return "It's a tie!"
        elif (
            (player_skill.display_name == "Rock" and bot_skill.display_name == "Scissors") or
            (player_skill.display_name == "Paper" and bot_skill.display_name == "Rock") or
            (player_skill.display_name == "Scissors" and bot_skill.display_name == "Paper")
        ):
            self.player_score += 1
            return "You win this round!"
        else:
            self.bot_score += 1
            return "Bot wins this round!"

    def _show_results(self):
        if self.player_score > self.bot_score:
            result = "Congratulations! You won the game!"
        elif self.bot_score > self.player_score:
            result = "The bot won the game. Better luck next time!"
        else:
            result = "The game ended in a tie!"

        self._show_text(self.player, result)
        self._show_text(self.player, f"Final Score - You: {self.player_score}, Bot: {self.bot_score}")

    def __str__(self):
        return f"Main Game: Round {self.rounds} - Your Score: {self.player_score}, Bot Score: {self.bot_score}"
