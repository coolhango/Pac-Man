import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from sound import Sound
from constants import *
from spritesheet import PacmanSprites


class Pacman(Sprite):
    def __init__(self, game, node, v=Vector()):
        super().__init__()
        self.game = game
        self.position = v
        self.settings = game.settings
        self.stats = game.stats
        self.sound = game.sound
        self.speed = self.settings.pacman_speed
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.directions = {
            STOP: Vector(),
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0),
        }
        self.direction = STOP
        initial_position = self.position.asInt()  # Get initial position as a tuple
        self.width_height = (5, 5)  # Width and height for collision
        self.rect = pg.Rect(initial_position, self.width_height)
        self.is_dying = False
        self.node = node
        self.set_position()
        self.target = node
        self.clock = pg.time.Clock()
        self.initial_node = node
        self.image = None
        self.sprites = PacmanSprites(game, self)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def set_position(self):
        self.position = self.node.position.copy()

    def die(self):
        self.alive = False
        self.direction = STOP
        self.sound.play_once("sounds/pacman_dying.wav")

    def reset(self):
        self.node = self.initial_node
        self.target = self.initial_node
        self.sprites.reset()
        self.set_position()
        self.direction = STOP
        self.alive = True

    def add_speed(self, speed):
        # if statements to prevent diagonal movement
        if speed.x != 0:
            self.position.x = speed.x
            self.position.y = 0
        elif speed.y != 0:
            self.position.y = speed.y
            self.position.x = 0

    def all_stop(self):
        self.position = Vector()

    def validate_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.validate_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def get_key(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_UP]:
            return UP
        if key_pressed[pg.K_DOWN]:
            return DOWN
        if key_pressed[pg.K_LEFT]:
            return LEFT
        if key_pressed[pg.K_RIGHT]:
            return RIGHT
        return STOP

    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def update(self, dt):
        if not self.alive:
            if self.sprites.animations[DEATH].finished:
                if self.stats.lives_left > 0:
                    self.reset()
                    self.game.restart()
                else:
                    self.game.game_over()

        self.sprites.update(dt)
        self.rect = pg.Rect(self.position.asInt(), self.width_height)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_key()

        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()
        self.draw()

    def draw(self):
        if self.image is not None:
            adjust = Vector(self.settings.tile_width, self.settings.tile_height) / 2
            p = self.position - adjust
            self.screen.blit(self.image, p.asTuple())
        else:
            p = self.position.asInt()
            pg.draw.circle(
                self.screen,
                YELLOW,
                p,
                self.settings.tile_width // 2,
            )


if __name__ == "__main__":
    print("\nERROR: pacman.py is the wrong file! Run play from game.py\n")
