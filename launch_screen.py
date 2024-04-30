import sys, time
import pygame as pg
from button import Button


class LaunchScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.stats = game.stats
        self.sound = game.sound
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 68)
        self.logo = pg.image.load("images/pac-man-logo.png")
        self.ghost_image = pg.image.load("images/ghosts.png")
        self.play_button = Button(
            game=self.game,
            text="Play",
            pos=(224, 500),
            size=(250, 70),
            selected_color=(57, 255, 20),
            bg_color=(255, 7, 58),
        )

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_q:
                    pg.quit()
                    sys.exit()
            elif type == pg.MOUSEBUTTONDOWN:
                b = self.play_button
                x, y = pg.mouse.get_pos()
                if b.rect.collidepoint(x, y):
                    b.press()
            elif type == pg.MOUSEMOTION:
                b = self.play_button
                x, y = pg.mouse.get_pos()
                b.select(b.rect.collidepoint(x, y))

    def display_logo(self):
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = self.screen_rect.centerx
        self.logo_rect.top = self.screen_rect.top + 30
        self.screen.blit(self.logo, self.logo_rect)

    def display_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"HIGHEST SCORE"

        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.logo_rect.bottom + 20

        high_score_value = f"{high_score:,}"

        self.high_score_value_image = self.font.render(
            high_score_value, True, (255, 223, 0), self.settings.bg_color
        )

        self.high_score_value_rect = self.high_score_value_image.get_rect()
        self.high_score_value_rect.centerx = self.screen_rect.centerx
        self.high_score_value_rect.top = self.high_score_rect.bottom + 5

        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.high_score_value_image, self.high_score_value_rect)

    def display_ghosts(self):
        self.ghost_image_rect = self.ghost_image.get_rect()
        self.ghost_image_rect.centerx = self.screen_rect.centerx
        self.ghost_image_rect.top = self.high_score_value_rect.bottom + 20
        self.screen.blit(self.ghost_image, self.ghost_image_rect)

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.display_logo()
        self.display_high_score()
        self.display_ghosts()
        self.play_button.update()
        pg.display.flip()

    def run(self):
        self.play_button.clicked = False
        self.play_button.show()
        if not pg.mixer.music.get_busy():
            self.sound.play_music("sounds/launch_theme.wav")
        while not self.game.game_active:
            self.draw()
            self.check_events()
            if self.play_button.clicked:
                self.game.play()
                break


if __name__ == "__main__":
    print("\nERROR: launch_screen.py is the wrong file! Run play from game.py\n")
