import sys, time
import pygame as pg

from settings import Settings
from vector import Vector
from game_stats import GameStats
from scoreboard import Scoreboard
from graph import NodeGroup
from sound import Sound
from pacman import Pacman
from pellets import PelletGroup
from ghosts import Ghosts
from launch_screen import LaunchScreen
from constants import *
from spritesheet import MazeSprites, LifeSprites


class Game:
    key_velocity = {
        pg.K_RIGHT: Vector(1, 0),
        pg.K_LEFT: Vector(-1, 0),
        pg.K_UP: Vector(0, -1),
        pg.K_DOWN: Vector(0, 1),
    }

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.screen_size, 0, 32)
        pg.display.set_caption("PAC-MAN")
        self.nodes = NodeGroup(game=self, level="maze_1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        home_key = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(home_key, (12, 14), LEFT)
        self.nodes.connectHomeNodes(home_key, (15, 14), RIGHT)
        self.sound = Sound(game=self)
        self.stats = GameStats(game=self)
        self.level = self.stats.level
        self.lifesprites = LifeSprites(game=self)
        self.sb = Scoreboard(game=self)
        self.launch_screen = LaunchScreen(game=self)
        self.game_active = False
        self.first = True
        self.pacman = Pacman(game=self, node=self.nodes.getNodeFromTiles(15, 26))
        nodes = list(self.nodes.nodesLUT.values())
        self.ghosts = Ghosts(game=self, node=nodes[10], pacman=self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.pellets = PelletGroup(game=self, pelletfile="maze_1.txt")
        self.clock = pg.time.Clock()
        self.goal = Vector()
        self.background = None
        self.maze_sprites = MazeSprites(
            game=self, mazefile="maze_1.txt", rotfile="maze_1_rotation.txt"
        )
        self.setBackground()

    def setBackground(self):
        self.background_norm = pg.surface.Surface(self.settings.screen_size).convert()
        self.background_norm.fill(self.settings.bg_color)
        self.background_norm = self.maze_sprites.constructBackground(
            self.background_norm, self.stats.level % 5 + 1
        )
        self.background = self.background_norm

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.KEYUP:
                key = event.key
            elif type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_q:
                    pg.quit()
                    sys.exit()

    def restart(self):
        self.screen.fill(self.settings.bg_color)
        self.setBackground()
        self.ghosts.reset()
        self.lifesprites.resetLives(self.stats.lives_left)
        self.screen.blit(self.background, (0, 0))
        self.sb.update()
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt=dt)
        self.ghosts.update(dt=dt)
        pg.display.flip()
        self.sound.play_start_up()

    def game_over(self):
        print("Game Over !")
        pg.mouse.set_visible(True)
        self.first = True
        self.game_active = False
        self.pellets = PelletGroup(game=self, pelletfile="maze_1.txt")
        self.stats.reset()
        self.sound.reset()
        self.launch_screen.run()

    def activate(self):
        self.game_active = True
        self.first = False

    def next_level(self):
        print(f"Level {self.stats.level} completed!")
        self.stats.level += 1
        print(f"Starting level {self.stats.level}")
        self.activate()
        self.restart()
        self.sb.prep_level()
        self.sb.prep_score()
        self.pellets = PelletGroup(game=self, pelletfile="maze_1.txt")
        self.pacman.reset()
        self.ghosts.reset()
        self.ghosts.blinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))

    def play(self):
        self.launch_screen.run()
        finished = False

        while not finished:
            self.check_events()  # exits if Cmd-Q on macOS or Ctrl-Q on other OS

            if self.game_active or self.first:
                if not pg.mixer.music.get_busy() and self.pacman.alive:
                    if len(self.pellets.pelletList) >= 150:
                        self.sound.play_music("sounds/ghost_siren.wav")
                    else:
                        self.sound.play_music("sounds/ghost_siren_2.wav")
                self.first = False
                self.screen.blit(self.background, (0, 0))
                self.sb.update()
                dt = self.clock.tick(30) / 1000.0
                self.pacman.update(dt=dt)
                self.pellets.update(dt=dt, pacman=self.pacman)
                self.ghosts.update(dt=dt)

            pg.display.flip()
            time.sleep(0.02)


if __name__ == "__main__":
    print("Welcome to PAC-MAN!")
    g = Game()
    g.play()
