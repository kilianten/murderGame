import pygame as pg
from settings import *
from collections import deque
import heapq
from sprites import Hitbox
vec = pg.math.Vector2

class Person(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.collidable_sprites, game.townspeople
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x + TILESIZE
        self.y = y + TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.dir = 0
        self.hitbox = Hitbox(self.rect)
        self.hitbox.setDimensions(-70,-80)
        self.grid = None
        self.path = None
        self.isWalking = False

    def vec2int(self, v):
        return (int(v.x), int(v.y))

    def update(self):
        self.rect.center = (self.x + TILESIZE/2, self.y)
        self.pos = vec(int(self.x/TILESIZE), int(self.y/TILESIZE))
        if self.isWalking:
            self.journey.update()

    def startJourney(self, start, destination, game):
        self.journey = Journey(start, destination, game)
        self.isWalking = True

    def drawPath(self):
        for node in self.journey.path:
            x, y = node
            rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE).move(self.game.camera.camera.topleft)
            pg.draw.rect(self.game.screen, LIGHTGREY, rect)
        current = self.journey.start + self.journey.path[self.vec2int(self.journey.start)]
        while current != self.journey.destination:
            x = current.x * TILESIZE + TILESIZE / 2
            y = current.y * TILESIZE + TILESIZE / 2
            img = self.game.arrows[self.vec2int(self.journey.path[(current.x, current.y)])]
            r = img.get_rect(center=(x, y))
            r = r.move(self.game.camera.camera.topleft)
            self.game.screen.blit(img, r)
            # find next in path
            current = current + self.journey.path[self.vec2int(current)]

class Journey:
    def __init__(self, start, destination, game):
        self.currentPos = start
        self.stepNumber = 0
        self.start = start
        self.destination = destination
        self.grid = WeightedGrid(game)
        self.path = self.grid.a_star_search(self.grid, start, destination)

    def update(self):
        if self.currentPos != self.destination:
            if self.currentPos != self.path:
                print(self.path)

class Priest(Person):
    pass

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

class SquareGrid:
    def __init__(self, game):
        self.game = game
        self.width = self.game.map.width/64
        self.height = self.game.map.height/64
        self.walls = []
        for wall in self.game.walls:
            self.walls.append(vec(wall.x, wall.y))
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        # don't use this for diagonals:
        if (node.x + node.y) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def vec2int(self, v):
        return (int(v.x), int(v.y))

    def heuristic(self, node1, node2):
        return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10

    def breadth_first_search(self, graph, start, end):
        frontier = deque()
        frontier.append(start)
        path = {}
        path[self.vec2int(start)] = None
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == end:
                break
            for next in graph.find_neighbors(current):
                if self.vec2int(next) not in path:
                    frontier.append(next)
                    path[self.vec2int(next)] = current - next
        return path

    def dijkstra_search(self, graph, start, end):
        frontier = PriorityQueue()
        frontier.put(self.vec2int(start), 0)
        path = {}
        cost = {}
        path[self.vec2int(start)] = None
        cost[self.vec2int(start)] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == end:
                break
            for next in graph.find_neighbors(vec(current)):
                next = self.vec2int(next)
                next_cost = cost[current] + graph.cost(current, next)
                if next not in cost or next_cost < cost[next]:
                    cost[next] = next_cost
                    priority = next_cost + self.heuristic(end, vec(next))
                    frontier.put(next, priority)
                    path[next] = vec(current) - vec(next)
        return path

    def a_star_search(self, graph, end, start):
        frontier = PriorityQueue()
        frontier.put(self.vec2int(start), 0)
        path = {}
        cost = {}
        path[self.vec2int(start)] = None
        cost[self.vec2int(start)] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == end:
                break
            for next in graph.find_neighbors(vec(current)):
                next = self.vec2int(next)
                next_cost = cost[current] + graph.cost(current, next)
                if next not in cost or next_cost < cost[next]:
                    cost[next] = next_cost
                    priority = self.heuristic(end, vec(next))
                    frontier.put(next, priority)
                    path[next] = vec(current) - vec(next)
        return path

class WeightedGrid(SquareGrid):
    def __init__(self, game):
        super().__init__(game)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 0) + 10
