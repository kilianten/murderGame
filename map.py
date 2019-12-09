import pygame as pg
from settings import *
from collections import deque
vec = pg.math.Vector2

class Map:
    def __init__(self, pathToImage):
        self.mapImage = pg.image.load(pathToImage).convert_alpha()
        self.tilewidth = self.mapImage.get_width()
        self.tileheight = self.mapImage.get_height()
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.rect = self.camera
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT/ 2)

        #limit scrolling to map TILESIZE
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.rect = self.camera
        print(self.rect.x)
        print(self.rect.y)

class CameraView:
    def __init__(self):
        self.camera = pg.Rect(0, 0, WIDTH, HEIGHT)

class SquareGrid:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.walls = []
        self.game = game
        self.connections = [vec(1,0), vec(-1, 0), vec(0,1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(self.game.screen, LIGHTGREY, rect.move(self.game.camera.camera.topleft))

    def vec2int(self,v):
        return (int(v[0]), int(v[1]))

    def breath_first_search(self, start, graph):
        frontier = deque()
        frontier.append(start)
        path = {}
        path[self.vec2int(start)] = None
        visited = []
        visited.append(self.vec2int(start))
        while len(frontier) > 0:
            current = frontier.popleft()
            for next in graph.find_neighbors(current):
                if self.vec2int(next) not in path:
                    frontier.append(next)
                    path[self.vec2int(next)] = current - next
        return path
