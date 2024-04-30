import pygame as pg
from settings import Settings


class Button:
    def __init__(
        self,
        game,
        text,
        pos=None,
        size=(200, 50),
        text_color=(255, 255, 255),
        selected_color=(57, 255, 250),
        bg_color=(57, 255, 20),
    ):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sb = game.sb
        self.screen_rect = self.screen.get_rect()
        self.text = text
        self.width, self.height = size[0], size[1]
        self.text_color = text_color
        self.bg_color = bg_color
        self.selected_color = selected_color
        self.font = pg.font.SysFont(None, 48)
        self.selected = False
        self.ensure_min_size()
        self.prep_text()

        # handle different position of button
        if pos:
            self.rect.center = pos
            self.image_rect.center = pos
        else:
            self.rect.center = self.screen_rect.center
            self.image_rect.center = self.rect.center

        self.visible = True
        self.clicked = False

    def __str__(self):
        return f"Just a button"

    def click(self):
        self.clicked = not self.clicked

    def select(self, selected):
        self.selected = selected

    def press(self):
        self.selected = False
        self.visible = False
        pg.mouse.set_visible(False)
        self.sb.prep()
        self.game.activate()
        self.game.restart()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def ensure_min_size(self):
        w, h = self.font.size(self.text)
        self.width = max(w + 2, self.width)
        self.height = max(h + 2, self.height)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def prep_text(self):
        self.notselected_img = self.font.render(
            self.text, True, self.text_color, self.bg_color
        )
        self.selected_img = self.font.render(
            self.text, True, self.text_color, self.selected_color
        )
        self.image = self.notselected_img if not self.selected else self.selected_img
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def update(self):
        self.image = self.notselected_img if not self.selected else self.selected_img
        self.draw()

    def draw(self):
        if not self.visible:
            return
        self.screen.fill(
            self.bg_color if not self.selected else self.selected_color, self.rect
        )
        self.screen.blit(self.image, self.image_rect)


if __name__ == "__main__":
    print("\nERROR: button.py is the wrong file! Run play from game.py\n")
