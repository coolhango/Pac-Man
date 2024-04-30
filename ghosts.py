import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector
from constants import *
from random import randint
from spritesheet import GhostSprites


class Ghost(Sprite):
    def __init__(self, game, node, pacman):
        super().__init__()
        self.name = None
        self.directions = {
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0),
            STOP: Vector(),
        }
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = Vector()
        # change this variable to goal_direction to make the ghost chase pacman
        # self.direction_method = self.random_direction
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
        self.set_start_node(node)
        self.image = None
        self.width_height = (5, 5)
        self.rect = pygame.Rect(self.position.asInt(), self.width_height)

    def set_start_node(self, node):
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def reset(self):
        self.set_position()
        self.is_dying = False
        self.mode.set_spawn_mode()

    def validate_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.validate_direction(direction):
            return self.node.neighbors[direction]
        return self.node

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

    def set_speed(self, speed):
        self.speed = speed * self.settings.tile_width / 16

    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validate_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = (
                self.node.position
                + self.directions[direction] * self.settings.tile_width
                - self.goal
            )
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    def update(self, dt):
        self.rect = pygame.Rect(self.position.asInt(), self.width_height)
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()
        self.draw(self.screen)

    def spawn(self):
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node):
        self.spawn_node = node

    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()

    def start_freight_mode(self):
        self.mode.start_freight()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self):
        self.set_speed(100)
        self.direction_method = self.goal_direction

    def choose_mode(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        self.update(dt)

    def scatter(self):
        self.goal = Vector()

    def chase(self):
        self.goal = self.pacman.position

    def draw(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector(self.settings.tile_width, self.settings.tile_height) / 2
                p = self.position - adjust
                self.screen.blit(self.image, p.asTuple())
                # screen.blit(self.image, self.position.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)


class Blinky(Ghost):
    def __init__(self, game, node, pacman=None):
        super().__init__(game, node, pacman)
        self.color = RED
        self.name = BLINKY
        self.sprites = GhostSprites(game, self)


class Pinky(Ghost):
    def __init__(self, game, node, pacman=None):
        super().__init__(game, node, pacman)
        self.color = PINK
        self.settings = game.settings
        self.name = PINKY
        self.sprites = GhostSprites(game, self)

    def scatter(self):
        self.goal = Vector(self.settings.tile_width * self.settings.board_cols, 0)

    def chase(self):
        self.goal = (
            self.pacman.position
            + self.pacman.directions[self.pacman.direction]
            * self.settings.tile_width
            * 4
        )


class Inky(Ghost):
    def __init__(self, game, node, pacman=None):
        super().__init__(game, node, pacman)
        self.color = TEAL
        self.settings = game.settings
        self.name = INKY
        self.sprites = GhostSprites(game, self)

    def scatter(self):
        self.goal = Vector(
            self.settings.tile_width * self.settings.board_cols,
            self.settings.tile_height * self.settings.board_rows,
        )

    def chase(self):
        self.goal = (
            self.pacman.position
            + self.pacman.directions[self.pacman.direction]
            * self.settings.tile_width
            * 2
        )


class Clyde(Ghost):
    def __init__(self, game, node, pacman=None):
        super().__init__(game, node, pacman)
        self.color = ORANGE
        self.settings = game.settings
        self.name = CLYDE
        self.sprites = GhostSprites(game, self)

    def scatter(self):
        self.goal = Vector(0, self.settings.tile_height * self.settings.board_rows)

    def chase(self):
        self.goal = (
            self.pacman.position
            + self.pacman.directions[self.pacman.direction]
            * self.settings.tile_width
            * 4
        )


class Ghosts:
    def __init__(self, game, node, pacman):
        self.game = game
        self.pacman = pacman
        self.nodes = game.nodes
        self.blinky = Blinky(game, node, pacman)
        self.pinky = Pinky(game, node, pacman)
        self.inky = Inky(game, node, pacman)
        self.clyde = Clyde(game, node, pacman)
        self.sb = game.sb
        self.stats = game.stats
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def update(self, dt):
        if self.pacman.alive:
            for ghost in self.ghosts:
                ghost.choose_mode(dt)
                if pygame.sprite.collide_circle(ghost, self.pacman):
                    if ghost.mode.current is FREIGHT:
                        ghost.start_spawn()
                        self.game.sound.play_eating_ghost()
                        self.stats.score += self.game.settings.ghost_points
                        self.sb.prep_score()
                        self.sb.check_high_score()
                    elif ghost.mode.current is not SPAWN:
                        if self.pacman.alive:
                            self.pacman.die()
                            self.stats.lives_left -= 1
                            self.game.lifesprites.removeImage()
                            self.reset()
                            self.blinky.set_start_node(
                                self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14)
                            )
                            self.pinky.set_start_node(
                                self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14)
                            )
                            self.inky.set_start_node(
                                self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14)
                            )
                            self.clyde.set_start_node(
                                self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14)
                            )

    def start_freight_mode(self):
        self.game.sound.stop_music()
        self.game.sound.play_music("sounds/power_pellet.wav")
        for ghost in self.ghosts:
            ghost.start_freight_mode()

    def set_spawn_node(self, node):
        for ghost in self.ghosts:
            ghost.set_spawn_node(node)

    def reset(self):
        for ghost in self.ghosts:
            ghost.reset()

    def hide(self):
        for ghost in self.ghosts:
            ghost.visible = False

    def show(self):
        for ghost in self.ghosts:
            ghost.visible = True


class MainMode:
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController:
    def __init__(self, ghost):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.ghost = ghost

    def start_freight(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def set_spawn_mode(self):
        if self.current is FREIGHT:
            self.current = SPAWN

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.ghost.game.sound.stop_music()
                self.ghost.normal_mode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode
        if self.current is SPAWN:
            if self.ghost.node == self.ghost.spawn_node:
                self.ghost.normal_mode()
                self.current = self.mainmode.mode


if __name__ == "__main__":
    print("\nERROR: ghost.py is the wrong file! Run play from game.py\n")
