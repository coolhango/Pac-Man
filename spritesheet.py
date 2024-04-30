import pygame as pg
from constants import *
from timer import Timer
import numpy as np


BASE_TILE_WIDTH = 16
BASE_TILE_HEIGHT = 16


class Spritesheet:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.tile_width = self.settings.tile_width
        self.tile_height = self.settings.tile_height
        self.sheet = pg.image.load("images/spritesheet.png").convert()
        transparent_color = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transparent_color)
        width = int(self.sheet.get_width() / BASE_TILE_WIDTH * self.tile_width)
        height = int(self.sheet.get_height() / BASE_TILE_HEIGHT * self.tile_height)
        self.sheet = pg.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= self.tile_width
        y *= self.tile_height
        self.sheet.set_clip(pg.Rect(x, y, width, height))
        # return self.sheet.subsurface(self.sheet.get_clip())
        image = self.sheet.subsurface(self.sheet.get_clip()).convert_alpha()
        image.set_colorkey(image.get_at((0, 0)))  # Set color key for each sprite
        return image


class PacmanSprites(Spritesheet):
    def __init__(self, game, pacman):
        super().__init__(game)
        self.pacman = pacman
        self.pacman.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(
            self, x, y, 2 * self.tile_width, 2 * self.tile_height
        )

    def defineAnimations(self):
        self.animations[LEFT] = Timer(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Timer(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Timer(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Timer(((8, 2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Timer(
            (
                (0, 12),
                (2, 12),
                (4, 12),
                (6, 12),
                (8, 12),
                (10, 12),
                (12, 12),
                (14, 12),
                (16, 12),
                (18, 12),
                (20, 12),
            ),
            speed=6,
            loop=False,
        )

    def update(self, dt):
        if self.pacman.alive == True:
            if self.pacman.direction == LEFT:
                self.pacman.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.pacman.direction == RIGHT:
                self.pacman.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.pacman.direction == DOWN:
                self.pacman.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.pacman.direction == UP:
                self.pacman.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.pacman.direction == STOP:
                self.pacman.image = self.getImage(*self.stopimage)
        else:
            self.pacman.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()


class GhostSprites(Spritesheet):
    def __init__(self, game, ghost):
        super().__init__(game)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.ghost = ghost
        self.ghost.image = self.getStartImage()
        self.ghost.rect = self.ghost.image.get_rect(center=self.ghost.position.asInt())

    def getStartImage(self):
        return self.getImage(self.x[self.ghost.name], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(
            self, x, y, 2 * self.tile_width, 2 * self.tile_height
        )

    def update(self, dt):
        x = self.x[self.ghost.name]
        if self.ghost.mode.current in [SCATTER, CHASE]:
            if self.ghost.direction == LEFT:
                self.ghost.image = self.getImage(x, 8)
            elif self.ghost.direction == RIGHT:
                self.ghost.image = self.getImage(x, 10)
            elif self.ghost.direction == DOWN:
                self.ghost.image = self.getImage(x, 6)
            elif self.ghost.direction == UP:
                self.ghost.image = self.getImage(x, 4)
        elif self.ghost.mode.current == FREIGHT:
            self.ghost.image = self.getImage(10, 4)
        elif self.ghost.mode.current == SPAWN:
            if self.ghost.direction == LEFT:
                self.ghost.image = self.getImage(8, 8)
            elif self.ghost.direction == RIGHT:
                self.ghost.image = self.getImage(8, 10)
            elif self.ghost.direction == DOWN:
                self.ghost.image = self.getImage(8, 6)
            elif self.ghost.direction == UP:
                self.ghost.image = self.getImage(8, 4)


class MazeSprites(Spritesheet):
    def __init__(self, game, mazefile, rotfile):
        super().__init__(game)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, self.tile_width, self.tile_height)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype="<U1")

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(
                        sprite, (col * self.tile_width, row * self.tile_height)
                    )
                elif self.data[row][col] == "=":
                    sprite = self.getImage(10, 8)
                    background.blit(
                        sprite, (col * self.tile_width, row * self.tile_height)
                    )
        return background

    def rotate(self, sprite, value):
        return pg.transform.rotate(sprite, value * 90)


class LifeSprites(Spritesheet):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.lives_left = self.game.stats.lives_left
        self.resetLives(self.lives_left)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, num_lives):
        self.images = []
        for i in range(num_lives):
            self.images.append(self.getImage(0, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(
            self, x, y, 2 * self.settings.tile_width, 2 * self.settings.tile_height
        )


if __name__ == "__main__":
    print("\nERROR: spritesheet.py is the wrong file! Run play from game.py\n")
