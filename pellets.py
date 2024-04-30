import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from constants import *
import numpy as np


class Pellet(Sprite):
    def __init__(self, game, row, column):
        super().__init__()
        self.settings = game.settings
        self.position = Vector(
            column * self.settings.tile_width, row * self.settings.tile_height
        )
        self.color = WHITE
        self.radius = int(2 * self.settings.tile_width / 16)
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position.asInt())
        self.points = self.settings.pellet_points
        self.visible = True

    def draw(self, screen):
        if self.visible:
            offset_x = 8  # Adjust the offset as needed
            offset_y = 4  # Adjust the offset as needed
            # Create a temporary rect for drawing at an offset position
            temp_rect = self.rect.copy()
            temp_rect.x += offset_x
            temp_rect.y += offset_y
            pg.draw.circle(
                self.image, self.color, (self.radius, self.radius), self.radius
            )
            screen.blit(self.image, temp_rect)


class PowerPellet(Pellet):
    def __init__(self, game, row, column):
        Pellet.__init__(self, game, row, column)
        self.radius = int(8 * self.settings.tile_width / 16)
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position.asInt())
        self.points = self.settings.power_pellet_points
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup:
    def __init__(self, game, pelletfile):
        self.game = game
        self.screen = game.screen
        self.ghosts = game.ghosts
        self.stats = game.stats
        self.sb = game.sb
        self.settings = game.settings
        self.pelletList = pg.sprite.Group()
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.num_eaten = 0

    def update(self, dt, pacman):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

        # Check for collisions
        collided_pellets = pg.sprite.spritecollide(
            pacman, self.pelletList, True, pg.sprite.collide_circle
        )
        for pellet in collided_pellets:
            if pellet in self.powerpellets:
                self.powerpellets.remove(pellet)
                # increase score here if it is a power pellet
                self.stats.score += self.settings.power_pellet_points
                # handle giving powers to pacman and making ghosts vulnerable
                self.ghosts.start_freight_mode()
            else:
                self.stats.score += self.settings.pellet_points
            self.game.sound.play_waka_waka()
            self.sb.prep_score()
            self.sb.check_high_score()
            self.num_eaten += 1
        # check if pelletlist is empty
        if self.isEmpty():
            # handle changing to next level
            self.game.next_level()

        self.draw(self.screen)

    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in [".", "+"]:
                    pellet = Pellet(self.game, row, col)
                    self.pelletList.add(pellet)
                elif data[row][col] in ["P", "p"]:
                    pp = PowerPellet(self.game, row, col)
                    self.pelletList.add(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def draw(self, screen):
        for pellet in self.pelletList:
            pellet.draw(screen)


if __name__ == "__main__":
    print("\nERROR: pellets.py is the wrong file! Run play from game.py\n")
