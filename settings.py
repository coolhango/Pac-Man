class Settings:
    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.lives = 3

        self.tile_width = 16
        self.tile_height = 16
        self.board_cols = 28
        self.board_rows = 36
        self.pacman_speed = 100 * self.tile_width / 16
        self.pellet_points = 10
        self.power_pellet_points = 50
        self.ghost_points = 200

        # was using 600 x 750
        self.screen_width = self.tile_width * self.board_cols
        self.screen_height = self.tile_height * self.board_rows
        self.screen_size = (self.screen_width, self.screen_height)


if __name__ == "__main__":
    print("\nERROR: settings.py is the wrong file! Run play from game.py\n")
