class GameStats:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.lives_left = 0
        self.reset()
        self.high_score = self.load_high_score()

    def reset(self):
        self.lives_left = self.settings.lives
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:
            with open("high_score.txt") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))


if __name__ == "__main__":
    print("\nERROR: game_stats.py is the wrong file! Run play from game.py\n")
