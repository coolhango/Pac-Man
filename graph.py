import pygame as pg
import numpy as np
from vector import Vector
from constants import *


class Node:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}

    def draw(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pg.draw.line(screen, WHITE, line_start, line_end, 4)
                pg.draw.circle(screen, RED, self.position.asInt(), 12)


class NodeGroup:
    def __init__(self, game, level):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.nodeList = []

        self.level = level
        # LUT = look up table
        self.nodesLUT = {}
        self.nodeSymbols = ["+", "P", "n"]
        self.pathSymbols = [".", "-", "|", "p"]
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.home_key = None

    def createHomeNodes(self, xoffset, yoffset):
        home_data = np.array(
            [
                ["X", "X", "+", "X", "X"],
                ["X", "X", ".", "X", "X"],
                ["+", "X", ".", "X", "+"],
                ["+", ".", "+", ".", "+"],
                ["+", "X", "X", "X", "+"],
            ]
        )
        self.createNodeTable(home_data, xoffset, yoffset)
        self.connectHorizontally(home_data, xoffset, yoffset)
        self.connectVertically(home_data, xoffset, yoffset)
        self.home_key = self.constructKey(xoffset + 2, yoffset)
        return self.home_key

    def connectHomeNodes(self, home_key, other_key, direction):
        key = self.constructKey(*other_key)
        self.nodesLUT[home_key].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction * -1] = self.nodesLUT[home_key]

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * self.settings.tile_width, y * self.settings.tile_height

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        other_key = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[other_key]
                        self.nodesLUT[other_key].neighbors[LEFT] = self.nodesLUT[key]
                        key = other_key
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        other_key = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[other_key]
                        self.nodesLUT[other_key].neighbors[UP] = self.nodesLUT[key]
                        key = other_key
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def update(self):
        for node in self.nodesLUT.values():
            node.draw(self.screen)


if __name__ == "__main__":
    print("\nERROR: graph.py is the wrong file! Run play from game.py\n")
